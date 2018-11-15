import math
import numpy

center_x = 0
center_y = 0

def circle_variance_cal(center_x = 0, center_y = 0, contour = []):
    mean_val = 0
    sum_sqrt = 0
    distance = []
    for element in contour:
       distance[] = numpy.sqrt(pow((element[0]-center_x),2) + pow((element[1]-center_y),2))
