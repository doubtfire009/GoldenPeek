import sys
import serial
import serial.tools.list_ports

from modbus import ModbusCmd, char_to_int16
from crc import crc16

port_list = list(serial.tools.list_ports.comports())
print(port_list[0][0])
port = serial.Serial(port=port_list[0][0], baudrate=19200, bytesize=8, parity='E', stopbits=1)



address = 0x01
regadd = 200
value = 3
send = ModbusCmd().cmd06(address, regadd, value)

port.write(send)
print(send)