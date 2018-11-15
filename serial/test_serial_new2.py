import serial
import easygui
import struct
import string
import binascii

ser = serial.Serial()
ser.baudrate = 19200  # 设置波特率（这里使用的是stc89c52）
ser.parity = 'E'  # 设置偶校验
ser.port = 'COM3'  # 端口是COM3

ser.open()  # 打开串口
print(ser.is_open)  # 检验串口是否打开
print(ser)
while (1):
    Yes_or_No = easygui.buttonbox("是否良品?", choices=['Yes', 'No', '退出'])  # 提供简易UI
    if Yes_or_No == '退出': break
    if Yes_or_No == 'Yes':
        # demo = b"2"  # 传入2的ASCII码 这里用b+str强制转换
        # values = (1)
        # string = ''
        # for i in values:
        #     string += struct.pack('!B', i)
        # 发送
        demo = bytes.fromhex('01 06 00 C8 00 02 48 35')
        print(demo)
        ser.write(demo)
        ser.read(1)
        ser.close()
    else:
        demo = b"1"  # 传入1的ASCII码 这里用b+str强制转换

