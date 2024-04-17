from crc import Calculator, Crc16
import serial
import time

ESTOP = b'\x06\x60\x02\x00\x40'     # Internal E-stop signal
SRV_ENBL = b'\x06\x20\x09\x00\x01'  # Internal servo enable
SRV_DSBL = b'\x06\x20\x09\x00\x00'  # Internal servo disable
TRG_P0 = b'\x06\x60\x02\x00\x20'    # Trigger path_0 motion (Movement mode)
TRG_HOM = b'\x06\x60\x02\x00\x20'   # Trigger path_0 motion (Homing mode)


crc = Calculator(Crc16.MODBUS,optimized=True)

try:
    ser = serial.Serial('/dev/uart/bone/4',115200)
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
    ValidateResponses([m1,m2,m3,m4],[r1,r2,r3,r4])
    
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
    SendQuadCommand(b'\x06\x60\x02\x00\x20') # Trigger homing
    # TODO: Implement a looping check for all servos to report homing complete.
    SendQuadCommand(ESTOP)
    SendQuadCommand(SRV_DSBL)
    # TODO: Report back to system that homing is complete.

    

def GetHeight():
    SendQuadCommand("read encoder")

SendQuadCommand(SRV_ENBL)
