
import serial
import serial.tools.list_ports
import settings.settings as settings

from modbus import ModbusCmd, char_to_int16



def modbusTransferrer(address=settings.modbusTransferAddress,regStart=settings.modbusTransferRegStart,value=0):
    portList = list(serial.tools.list_ports.comports())
    print(portList[0][0])
    port = serial.Serial(port=portList[0][0], baudrate=19200, bytesize=8, parity='E', stopbits=1)

    print(port.is_open)  # 检验串口是否打开

    send = ModbusCmd().cmd03(address, regStart, value)


    port.write(send)


def modbusListTransferrer(resList = []):
    ret = 0
    if resList:
        if resList[0][0]>0:
            for item in resList:
                i = resList.index(item)
                modbusTransferrer(settings.modbusTransferAddress,settings.modbusTransferRegStart + i*settings.modbusTransferIntval)
                modbusTransferrer(settings.modbusTransferAddress,settings.modbusTransferRegStart + i*settings.modbusTransferIntval + settings.modbusTransferXYIntval)
            ret = 1
    else:
        ret = -1
    return ret


def recvWatchDog():
    while True:
        watchDog = serial.read(1)
        if data == '':
            continue
        else:
            break
        sleep(0.5)
    return watchDog