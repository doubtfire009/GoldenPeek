import cv2
import numpy as np
import settings.settings as settings

# test = [[178.5, 188.5, 22.100000381469727], [526.5, 283.5, 23.5]]
#
# testM = np.array(test)
#
# print(testM)
# print(testM.ndim)
# print(testM.shape)

def isint(aString):
    try:
        if int(aString)>0 :
            return True
        else:
            return False
    except:
        return False

print(isint("-1"))