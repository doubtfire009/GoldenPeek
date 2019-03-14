import cv2
import numpy as np
import settings.settings as settings
import datetime
import time

# test = [[178.5, 188.5, 22.100000381469727], [526.5, 283.5, 23.5]]
#
# testM = np.array(test)
#
# print(testM)
# print(testM.ndim)
# print(testM.shape)

# def isint(aString):
#     try:
#         if int(aString)>0 :
#             return True
#         else:
#             return False
#     except:
#         return False
#
# print(isint("-1"))

# date1Cutter = "2019-02-20"
# date2Cutter = "2019-03-20"
# date1 = datetime.datetime.strptime(date1Cutter,'%Y-%m-%d').date()
# date2 = datetime.datetime.strptime(date2Cutter,'%Y-%m-%d').date()
# print(date1>date2)

# dateCutter = "2019-03-20"
# dateCutter = datetime.datetime.strptime(dateCutter,'%Y-%m-%d').date()
dateCutter = datetime.datetime(2019, 3, 20)

nowTime = datetime.datetime.now()

print(dateCutter > nowTime)
