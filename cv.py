import cv2
import numpy as np

def convert_gray_scale(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    hsv=cv2.resize(hsv,(300,300))
    return hsv

