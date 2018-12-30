
import serial
import serial.tools.list_ports

from modbus import ModbusCmd, char_to_int16



def modbusTransferrer(address=0x01,regStart=600,value=0):
    portList = list(serial.tools.list_ports.comports())
    print(portList[0][0])
    port = serial.Serial(port=portList[0][0], baudrate=19200, bytesize=8, parity='E', stopbits=1)

    print(port.is_open)  # 检验串口是否打开

    send = ModbusCmd().cmd03(address, regStart, value)


    port.write(send)