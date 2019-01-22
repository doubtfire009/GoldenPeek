import sys
import serial
import serial.tools.list_ports

from modbus import ModbusCmd, char_to_int16
from crc import crc16

import time

port_list = list(serial.tools.list_ports.comports())
print(port_list[0][0])
port = serial.Serial(port=port_list[0][0], baudrate=19200, bytesize=8, parity='E', stopbits=1)

print(port.is_open)  # 检验串口是否打开


def recv(serial):
  while True:
    data =serial.read(1)
    if data == '':
      continue
    else:
      break
    sleep(0.02)
  return data


address = 0x01
reg_start = 5
reg_count = 1
send = ModbusCmd().cmd03(address, reg_start, reg_count)

port.write(send)
print(send)

s = b'\n'
print(s)
print(len(s))

time.sleep(10)
while True:
    data =recv(port)
    if data != '':
        print(data)






