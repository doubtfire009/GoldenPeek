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


finderProcessResult = []

modbusTransferXYIntval = 10
modbusTransferIntval = 50
modbusTransferAddress = 0x01
modbusTransferRegStart = 500


modbusWatchDog = 7788

autoCease = 0
autoLaunchMachineCounter = 0
autoCatchIntval = 1050