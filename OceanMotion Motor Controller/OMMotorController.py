from crc import Calculator, Crc16
import serial
import time

ESTOP = b'\x06\x60\x02\x00\x40'       # Internal E-stop signal
SRV_ENBL = b'\x06\x20\x09\x00\x01'    # Internal servo enable
SRV_DSBL = b'\x06\x20\x09\x00\x00'    # Internal servo disable
SRV_STAT = b'\x03\x60\x02\x00\x01'    # Read command, returns whether the operating status of a given servo
SRV_RDY = b'\x03\x60\x02\x02\x00\x00' # Servo status indicating it is ready for additional commands.
TRG_P0 = b'\x06\x60\x02\x00\x20'      # Trigger path_0 motion (Movement mode)
TRG_HOM = b'\x06\x60\x02\x00\x20'     # Trigger path_0 motion (Homing mode)


crc = Calculator(Crc16.MODBUS,optimized=True)

try:
    ser = serial.Serial('/dev/bone/uart/4',115200)
    ser.close()
    ser.open()
except:
    print("No Serial Port Found...")
    #exit()

def SendQuadCommand(command): # Adjusts a command to send to all 4 actuators (adr 1-4) with a period of 2ms
    m1 = bytearray([0x01])
    m1.extend(command)
    m1.extend(crc.checksum(m1).to_bytes(2,'little'))
    ser.write(m1)
    time.sleep(0.001)
    r1 = ser.read()
    time.sleep(0.001)
    m2 = bytearray([0x02])
    m2.extend(command)
    m2.extend(crc.checksum(m2).to_bytes(2,'little'))
    ser.write(m2)
    time.sleep(0.001)
    r2 = ser.read()
    time.sleep(0.001)
    m3 = bytearray([0x03])
    m3.extend(command)
    m3.extend(crc.checksum(m3).to_bytes(2,'little'))
    ser.write(m3)
    time.sleep(0.001)
    r3 = ser.read()
    time.sleep(0.001)
    m4 = bytearray([0x04])
    m4.extend(command)
    m4.extend(crc.checksum(m4).to_bytes(2,'little'))
    ser.write(m4)
    time.sleep(0.001)
    r4 = ser.read()
    time.sleep(0.001)
    #ValidateResponses([m1,m2,m3,m4],[r1,r2,r3,r4])

def SendQuadRead(command): # Adjusts a read request to send to all 4 actuators (adr 1-4) with a period of 2ms
    m1 = bytearray([0x01])
    m1.extend(command)
    m1.extend(crc.checksum(m1).to_bytes(2,'little'))
    ser.write(m1)
    time.sleep(0.001)
    r1 = ser.read()
    time.sleep(0.001)
    m2 = bytearray([0x02])
    m2.extend(command)
    m2.extend(crc.checksum(m2).to_bytes(2,'little'))
    ser.write(m2)
    time.sleep(0.001)
    r2 = ser.read()
    time.sleep(0.001)
    m3 = bytearray([0x03])
    m3.extend(command)
    m3.extend(crc.checksum(m3).to_bytes(2,'little'))
    ser.write(m3)
    time.sleep(0.001)
    r3 = ser.read()
    time.sleep(0.001)
    m4 = bytearray([0x04])
    m4.extend(command)
    m4.extend(crc.checksum(m4).to_bytes(2,'little'))
    ser.write(m4)
    time.sleep(0.001)
    r4 = ser.read()
    time.sleep(0.001)
    return [r1,r2,r3,r4]
    
def ValidateResponses(messages,responses):  # If any response ever fails to match the sent command, the program is halted.
    for i in 3:
        if messages[i] != responses[i]:
            print("Command " + messages[i] + "doesn't match response " + responses[i])
            SendQuadCommand(ESTOP)
            exit(-1)

def RunHomingSequence():
    SendQuadCommand(SRV_ENBL)
    SendQuadCommand(b'\x06\x60\x14\x00\x0a') # Set homing torque to 10%.
    SendQuadCommand(b'\x06\x60\x0a\x00\x0c') # Set negative homing direction, don't go to set position after homing, homing with torque detect.
    SendQuadCommand(b'\x06\x60\x0f\x01\x90') # Set homing high speed to 400 rpm
    SendQuadCommand(b'\x06\x60\x10\x00\x64') # Set homing low speed to 100 rpm
    SendQuadCommand(TRG_HOM) # Trigger homing
    WaitTillReady()
    SendQuadCommand(ESTOP)
    SendQuadCommand(SRV_DSBL)
    # TODO: Report back to system that homing is complete.

def SetPosition(height: float, speed: int):
    height = (height*3*10000).to_bytes(4,'big') # multiply desired height by rotations per mm * 10000 pulses per rotation
    speed = speed.to_bytes(2,'big')
    SendQuadCommand(SRV_ENBL)                     # Enable servos
    SendQuadCommand(b'\x06\x62\x00\x00\x01')      # Set absolute positioning mode.
    SendQuadCommand(b'\x06\x62\x01'+height[:-2])  # Set pos in pulses (high 2 bytes)
    SendQuadCommand(b'\x06\x62\x02'+height[2:])   # Set pos in pulses (low 2 bytes)
    SendQuadCommand(b'\x06\x62\x03'+speed)        # Set speed in rpm
    SendQuadCommand(b'\x06\x62\x04\x00\x32')      # Set acceleration to 50ms/1000rpm
    SendQuadCommand(b'\x06\x62\x05\x00\x32')      # Set deceleration to 50ms/1000rpm
    SendQuadCommand(TRG_P0)                       # Trigger path_0 motion
    WaitTillReady()                               # Wait till all actuators reach given position
    SendQuadCommand(ESTOP)                        # Estop signal
    SendQuadCommand(SRV_DSBL)                     # Disable servos

def RunPositionSequence(positions: list):
    SendQuadCommand(SRV_ENBL)                     # Enable servos
    SendQuadCommand(b'\x06\x62\x00\x00\x01')      # Set absolute positioning mode.
    SendQuadCommand(b'\x06\x62\x03\x02\x58')      # Set speed to 600 rpm 
    SendQuadCommand(b'\x06\x62\x04\x00\x32')      # Set acceleration to 50ms/1000rpm
    SendQuadCommand(b'\x06\x62\x05\x00\x32')      # Set deceleration to 50ms/1000rpm
    for p in positions:
        p = (p*3*10000).to_bytes(4,'big')
        SendQuadCommand(b'\x06\x62\x01'+p[:-2])   # Set pos in pulses (high 2 bytes)
        SendQuadCommand(b'\x06\x62\x02'+p[2:])    # Set pos in pulses (low 2 bytes)
        SendQuadCommand(TRG_P0)                   # Trigger path_0 motion
        WaitTillReady()                           # Wait till all actuators reach given position
    SendQuadCommand(ESTOP)                        # Estop signal
    SendQuadCommand(SRV_DSBL)                     # Disable servos


def WaitTillReady():
    resp = b'\xff\xff\xff\xff\xff\xff'
    while resp != SRV_RDY:
        responses = SendQuadRead(SRV_STAT)
        for r in responses:
            r = r[1:-2] # Removes the address byte and crc bytes
            resp = resp & r # ands all 4 responses together, if result equals SRV_RDY status, then all 4 are ready

def GetHeight():
    SendQuadCommand("read encoder")
