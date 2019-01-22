import sys
import serial
import serial.tools.list_ports

from modbus import ModbusCmd, char_to_int16
from crc import crc16

port_list = list(serial.tools.list_ports.comports())
print(port_list[0][0])
port = serial.Serial(port=port_list[0][0], baudrate=19200, bytesize=8, parity='E', stopbits=1)


def recv(serial):
  while True:
    data =serial.read(1)
    if data == '':
      continue
    else:
      break
    sleep(0.02)
  return data

# address = 0x01
# regadd = 100
# value = 300

# address = 0x01
# regadd = 80
# value = 7
# send = ModbusCmd().cmd06(address, regadd, value)
#
# port.write(send)
# print(send)

address = 0x01
regadd = 30
reg_count = 2
value = [10,11]
send = ModbusCmd().cmd10(address, regadd,reg_count, value)

port.write(send)
print(send)

while True:
    data =recv(port)
    if data != '':
        print(data)