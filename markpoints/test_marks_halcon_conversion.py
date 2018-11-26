import cv2
import math

theta = 0
a = 0
b = 0

def marksHalconReverseConverter():


def marksHalconConverter(A1 = (0,0),A2 = (0,0)):
    # x=x'·cos(θ)+y'·sin(θ)+a
    # y=y'·cos(θ)-x'·sin(θ)+b
    A2[0] = A1[0] * math.cos(theta) + A1[1] * math.sin(theta) + a
    A2[1] = A1[1] * math.cos(theta) - A1[0] * math.sin(theta) + b

    return A2




