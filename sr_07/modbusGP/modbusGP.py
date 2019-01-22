
import serial
import serial.tools.list_ports
import settings.settings as settings
import time
import struct

from modbusGP.modbus import ModbusCmd, char_to_int16

def portBuilder():
    portList = list(serial.tools.list_ports.comports())

    port = serial.Serial(port=portList[0][0], baudrate=19200, bytesize=8, parity='E', stopbits=1)

    # print(port.is_open)  # 检验串口是否打开
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


def modbusAutoTransferrer(port,regStart=settings.modbusTransferRegStart,value=0):
    # address = settings.modbusTransferAddress
    address = 0x01
    send = ModbusCmd().cmd06(address, regStart, value)
    port.write(send)


def modbusAutoListTransferrer(port,regStart = settings.modbusTransferRegStart, regCount = 1, list=[0]):
    address = settings.modbusTransferAddress

    send = ModbusCmd().cmd10(address, regStart, regCount, list)
    port.write(send)





def recvWatchDog(port, regStart, regCount=1, forceZero = False):

    address = settings.modbusTransferAddress
    settings.watchDogReg = -1
    if forceZero == True:
        settings.watchDogCounter = 0

    #看门狗计数器为0，则发送读取信号
    if settings.watchDogCounter == 0:
        readSignal = ModbusCmd().cmd03(address, regStart, regCount)
        port.write(readSignal)

    #其他时间都持续获取串口信息
    else:
        watchDogReg = port.read(1)
        # if watchDogReg != b'\n':
        #     settings.watchDogRegList.append(watchDogReg)
        settings.watchDogRegList.append(watchDogReg)

    settings.watchDogCounter = settings.watchDogCounter + 1

    if settings.watchDogCounterThresh < settings.watchDogCounter:
        settings.watchDogCounter = 0
        settings.watchDogRegList = []

    if len(settings.watchDogRegList)==2:
        if settings.watchDogRegList[0] == b'\x01':
            if settings.watchDogRegList[1] ==  b'\x10':
                settings.watchDogRegListLenReq = 8
            else:
                settings.watchDogRegListLenReq = 7
        else:
            settings.watchDogRegList = []

    if len(settings.watchDogRegList) == settings.watchDogRegListLenReq:
        #其他写响应的信息都不要
        if settings.watchDogRegList[1] == b'\x03':
            settings.watchDogReg = settings.watchDogRegList[settings.watchDogRegListLenReq - 3]
            # 这句话是将b'\x1f'转化成31，int类型的关键语句
            settings.watchDogReg = settings.watchDogReg[0]

        #极其关键！不然会有死锁！
        settings.watchDogCounter = 0
        # 极其关键！不然会空转
        settings.watchDogRegList = []
    # else:
    #     settings.watchDogReg = -1

    return settings.watchDogReg