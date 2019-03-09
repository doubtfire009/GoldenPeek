#coding=utf-8

import cv2
import numpy as np

#image for tkinter
canvasWidth = 0
canvasHeight = 0

delay = 15

#btn_catch
showing_frame=1
click_frame = 0

#image displayer
INIT = 'init'
CATCHED = 'catched'
HALCON = 'halcon'
PROCESSED = 'processed'

displayerFlag = INIT

#Halcon Points

halconReview = []

#Halcon constants
halconThreshold = 0
halCosTheta = 0
halSinTheta = 0
halA = 0
halB = 0

halconConverterMatrix = [[0,0],[0,0]]

halconConverterX = [0,0]
halconConverterY = [0,0]

#Processor Flags
processCatcherFlag = 0
processorImageFlag = 0
processModbusFlag = 0
processThreshold = 0


catch_img_dir = './images_storage/catched/'
halcon_img_dir = './images_storage/halcon/'
process_img_dir = './images_storage/processed/'

#halcon circles
halconCircle = []

#Halcon X-Y
halcon_A = [0,0]
halcon_B = [0,0]
halcon_C = [0,0]
halcon_D = [0,0]

halconHoughParam1 = 50
halconHoughParam2 = 30

#threshold types

thresholdType = ['cal','area']
thresholdSource = ['halcon','finder']
thresholdLevel = ['low','high']

thresholdInfo = {
    'halcon':
        {'halcon':
             {
                'halconHoughParam1':100,
                'halconHoughParam2':30,
                'halconHoughminRadius':1,
                'halconHoughmaxRadius':1
             },
        'cal':
             {
                 'low': 0,
                 'high':0
             }
         },
    'finder':
        {'cal':
            {
                'low': 0,
                'high': 0
            },

        'area':
            {
                'low': 0,
                'high': 0
            },
        'hough':
            {
                'halconHoughminRadius':1,
                'halconHoughmaxRadius': 1
            }
        },
    'autoFinder':
        {'cal':
            {
                'low': 0,
                'high': 0
            },

        'area':
            {
                'low': 0,
                'high': 0
            }
        }
    }


processType = 'default'

processCircle = []

# finderProcessResult = [[12,34],[78,91],[7,18]]
finderProcessResult = []

modbusTransferXYIntval = 10
modbusTransferIntval = 50
modbusTransferAddress = 0x01
modbusTransferRegStart = 500


modbusWatchDog = 7788

autoSwitch = 0
autoCease = 0
autoLaunchMachineCounter = 0
autoCatchIntval = 1050


############################################
### Modbus Robots Communication Settings####
############################################

##主被动状态
# workStatus=0时候，程序监听modbus
# workStatus=1时候，程序自己处理数据
workStatus = False


##阶段标志位偏移数
stepIndicatorReg = 43

#开始阶段
stepStart = 0
#电脑处理阶段（截图，处理）
stepImgProcess = 1
#抓取阶段
stepRobot = 2

#状态总数
stepNum = 3

#电脑处理所处阶段
stepRequired = 0

stepNow= 0
#获取的阶段寄存器数值
stepIndicator = 0

#电脑处理阶段内部是否完成的标志,
# stepNum包含的阶段，每个阶段开始时候置0，完成置1
stepFinish1 = 0
stepFinish2 = 0


#坐标数据就绪标志位偏移数
coordinateReadyReg = 35
#取出的坐标数据就绪标志位数值
coordinateReady = 0

#坐标数据存储区偏移数
XDataStore = 30
YDataStore = 31

#看门狗调度计数器
watchDogCounter = 0
#看门狗计数器阈值（过此数值则归零）
watchDogCounterThresh = 200
#看门狗返回值
watchDogReg = 0
#看门狗返回值的数组
watchDogRegList = []
#看门狗返回值的数组合法长度
watchDogRegListLenReq = 7