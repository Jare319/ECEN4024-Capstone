from crc import Calculator, Crc16
import serial
import time

ESTOP = b'\x06\x60\x02\x00\x40'     # Internal E-stop signal
SRV_ENBL = b'\x06\x20\x09\x00\x01'  # Internal servo enable
SRV_DSBL = b'\x06\x20\x09\x00\x00'  # Internal servo disable
SRV_STAT = b'\x03\x60\x02\x00\x01'  # Read command, returns whether the operating status of a given servo
SRV_RDY = b'\x03\x02\x00\x00'       # Servo status indicating it is ready for additional commands.
TRG_P0 = b'\x06\x60\x02\x00\x10'    # Trigger path_0 motion (Movement mode)
TRG_HOM = b'\x06\x60\x02\x00\x20'   # Trigger path_0 motion (Homing mode)

crc = Calculator(Crc16.MODBUS,optimized=True)

try:
    ser = serial.Serial('/dev/bone/uart/4',115200)
    ser.close()
    ser.open()
except:
    print("No Serial Port Found...")
    exit(-1)

def SendSingleCommand(command: bytes, retries:int): # Sends a single command, used for correcting errors.
    attempt = 0
    while attempt < retries:
        ser.write(command)
        time.sleep(0.02)
        r = ser.read_all()
        time.sleep(0.02)
        if r == command:
            return
        else:
            print("Transmission error detected...\nCommand: "+str(command)+"\nResponse: "+str(r))
            attempt += 1
    print("Error could not be handled. Halting actuators...")
    SendQuadCommand(ESTOP) # Yes, in theory this could infinitely recurse
    exit(-69)

def BuildCommand(command:bytes, addr:int) -> bytes:
    m = addr.to_bytes(1,'big')+command
    m = m+crc.checksum(m).to_bytes(2,'little')
    return bytes(m)

def SendQuadCommand(command,retries=2): # Adjusts a command to send to all 4 actuators (adr 1-4) with a period of 2ms
    SendSingleCommand(BuildCommand(command,1),retries)
    SendSingleCommand(BuildCommand(command,2),retries)
    SendSingleCommand(BuildCommand(command,3),retries)
    SendSingleCommand(BuildCommand(command,4),retries)

def SendQuadRead(command): # Adjusts a read request to send to all 4 actuators (adr 1-4) with a period of 2ms
    m1 = bytearray([0x01])
    m1.extend(command)
    m1.extend(crc.checksum(m1).to_bytes(2,'little'))
    ser.write(m1)
    time.sleep(0.01)
    r1 = ser.read_all()
    time.sleep(0.01)
    m2 = bytearray([0x02])
    m2.extend(command)
    m2.extend(crc.checksum(m2).to_bytes(2,'little'))
    ser.write(m2)
    time.sleep(0.01)
    r2 = ser.read_all()
    time.sleep(0.01)
    m3 = bytearray([0x03])
    m3.extend(command)
    m3.extend(crc.checksum(m3).to_bytes(2,'little'))
    ser.write(m3)
    time.sleep(0.01)
    r3 = ser.read_all()
    time.sleep(0.01)
    m4 = bytearray([0x04])
    m4.extend(command)
    m4.extend(crc.checksum(m4).to_bytes(2,'little'))
    ser.write(m4)
    time.sleep(0.01)
    r4 = ser.read_all()
    time.sleep(0.01)
    return [r1,r2,r3,r4]

def RunHomingSequence():
    SendQuadCommand(SRV_ENBL)
    SendQuadCommand(b'\x06\x60\x14\x00\x08') # Set homing torque to 8%.
    SendQuadCommand(b'\x06\x60\x0a\x00\x0c') # Set negative homing direction, don't go to set position after homing, homing with torque detect.
    SendQuadCommand(b'\x06\x60\x0f\x01\x90') # Set homing high speed to 400 rpm
    SendQuadCommand(b'\x06\x60\x10\x00\x64') # Set homing low speed to 100 rpm
    SendQuadCommand(TRG_HOM) # Trigger homing
    WaitTillReady()
    SendQuadCommand(ESTOP)
    SendQuadCommand(SRV_DSBL)
    SendQuadCommand(SRV_DSBL)
    # TODO: Report back to system that homing is complete.

def SetPosition(height: int, speed: int):
    height = (int)((height/3)*10000).to_bytes(4,'big') # multiply desired height by rotations per mm * 10000 pulses per rotation
    speed = speed.to_bytes(2,'big')
    SendQuadCommand(SRV_ENBL)                     # Enable servos
    SendQuadCommand(b'\x06\x62\x00\x00\x01')      # Set absolute positioning mode.
    SendQuadCommand(b'\x06\x62\x01'+height[:-2])  # Set pos in pulses (high 2 bytes)
    SendQuadCommand(b'\x06\x62\x02'+height[2:])   # Set pos in pulses (low 2 bytes)
    SendQuadCommand(b'\x06\x62\x03'+speed)        # Set speed in rpm
    SendQuadCommand(b'\x06\x62\x04\x00\x32')      # Set acceleration to 50ms/1000rpm
    SendQuadCommand(b'\x06\x62\x05\x00\x32')      # Set deceleration to 50ms/1000rpm
    SendQuadCommand(TRG_P0)                       # Trigger path_0 motion
    WaitTillReady()
    #time.sleep(10)                               # Wait till all actuators reach given position
    SendQuadCommand(ESTOP)                        # Estop signal
    SendQuadCommand(SRV_DSBL)                     # Disable servos

def RunPositionSequence(positions: list, period: int):
    SendQuadCommand(SRV_ENBL)                     # Enable servos
    vel = int(vel).to_bytes(2,'big')
    pos = int((positions[0]/3)*10000).to_bytes(4,'big')
    accel = "placeholder"
    # Bulk send commands: Mode, High pos, Low pos, Speed, Accel, Decel, Delay, Trigger
    SendQuadCommand(b'\x10\x62\x00\x00\x08\x00\x01'+pos[:-2]+pos[2:]+b'\x0b\xb8'+accel+accel+b'\x00\x00'+TRG_P0)  
    time.sleep(period)
    for i in range(1,len(positions)):
        p = int(((positions[i]/3)*10000)).to_bytes(4,'big')
        a = "placeholder"
        SendQuadCommand(b'\x10\x62\x00\x00\x08\x00\x01'+p[:-2]+p[2:]+b'\x0b\xb8'+a+a+b'\x00\x00'+TRG_P0)
        time.sleep(period)
    WaitTillReady()
    SendQuadCommand(ESTOP)                        # Estop signal
    SendQuadCommand(SRV_DSBL)                     # Disable servos

def WaitTillReady():
    while True:
        responses = SendQuadRead(SRV_STAT)
        if all(i[1:-2] == SRV_RDY for i in responses):
            break

def GetHeight():
    SendQuadCommand("read encoder")

print("Homing...")
RunHomingSequence()
time.sleep(3)
print("Positioning...")
#SetPosition(300, 600)
RunPositionSequence()
