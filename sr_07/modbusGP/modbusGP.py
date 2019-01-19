
import serial
import serial.tools.list_ports
import settings.settings as settings
import time

from modbusGP.modbus import ModbusCmd, char_to_int16

def portBuilder():
    portList = list(serial.tools.list_ports.comports())
    print(portList[0][0])
    port = serial.Serial(port=portList[0][0], baudrate=19200, bytesize=8, parity='E', stopbits=1)

    print(port.is_open)  # 检验串口是否打开
    return port

def modbusTransferrer(address=settings.modbusTransferAddress,regStart=settings.modbusTransferRegStart,value=0):
    port = portBuilder()

    send = ModbusCmd().cmd06(address, regStart, value)

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


def recvWatchDog(port, regStart, regCount=1):

    address = 0x01
    #看门狗计数器为0，则发送读取信号
    if settings.watchDogCounter == 0:
        readSignal = ModbusCmd().cmd03(address, regStart, regCount)
        print(readSignal)
        watchDog = 0
    #其他时间都持续获取串口信息
    else:
        watchDog = port.read(1)

    settings.watchDogCounter = settings.watchDogCounter + 1

    if settings.watchDogCounterThresh < settings.watchDogCounter:
        settings.watchDogCounter = 0



    return watchDog