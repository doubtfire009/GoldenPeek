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
xMax_y = [0,0]
xMin_y = [0,0]
x_yMax = [0,0]
x_yMin = [0,0]

halconReview = [xMax_y,xMin_y,x_yMax,x_yMin]

#Halcon constants
halconThreshold = 0
halCosTheta = 0
halSinTheta = 0
halA = 0
halB = 0

halconConverterMatrix = np.matrix([
    [2,1],
    [0,3]
])

#Processor Flags
processCatcherFlag = 0
processorImageFlag = 0
processModbusFlag = 0
processThreshold = 0


catch_img_dir = './images_storage/catched/'
halcon_img_dir = './images_storage/halcon/'
process_img_dir = './images_storage/processed/'


#Halcon X-Y
halcon_A = [0,0]
halcon_B = [0,0]
halcon_C = [0,0]
halcon_D = [0,0]

#threshold types

thresholdType = ['cal','area']
thresholdSource = ['halcon','finder']
thresholdLevel = ['low','high']

thresholdInfo = {
    'halcon':
        {'cal':
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


# finderProcessResult = [[12,34],[78,91],[7,18]]
finderProcessResult = [[7,18]]

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
stepIndicatorReg = 5

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
stepFinish = 0


#坐标数据就绪标志位偏移数
coordinateReadyReg = 10
#在抓取阶段：坐标数据是否读取过
coordinateReadyFinish = 0

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