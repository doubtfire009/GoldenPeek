import cv2
import numpy as np
import math

cosTheta = 0
sinTheta = 0
a = 0
b = 0

# x=x'·cos(θ)+y'·sin(θ)+a
# y=y'·cos(θ)-x'·sin(θ)+b

def AListHalconBuilder(A1 = (0,0),A2 = (0,0)):
    AListHalcon = np.matrix(
        [[A1[0], A1[1], 1, 0],
         [A1[1], (-1) * A1[0], 0, 1],
         [A2[0], A2[1], 1, 0],
         [A2[1], (-1) * A2[0], 0, 1]]
    )
    return AListHalcon



def marksHalconReverseConverter(A1 = (0,0),A2 = (0,0),B1 = (0,0),B2 = (0,0)):
    BList = np.matrix([B1[0],
                   B1[1],
                    B2[0],
                    B2[1]])
    BList = BList.T
    print(BList)

    AListHalcon = AListHalconBuilder(A1,A2)

    MatrixHalcon = ((AListHalcon.I)*BList).T

    ArrayHalcon = MatrixHalcon.tolist()
    return ArrayHalcon[0]

def constHalconSetter(ArrayHalcon):
    global cosTheta
    cosTheta = ArrayHalcon[0]
    global sinTheta
    sinTheta = ArrayHalcon[1]
    global a
    cosTheta = ArrayHalcon[2]
    global b
    sinTheta = ArrayHalcon[3]

def HalconConverterBuilder(A = (0,0)):
    B1[0] = A1[0] * cosTheta + A1[1] * cosTheta + a
    B1[1] = A1[1] * sinTheta - A1[0] * sinTheta + b
    return B1

A1 = (540.0, 320.0)
A2 = (60.0, 80.0)

B1 = (112,30)
B2 = (80,440)

marksHalconReverseConverter(A1,A2,B1,B2)

test = np.matrix([
    [1,0,0],
    [0,1,0],
    [0,0,8]
])

print(test.I)