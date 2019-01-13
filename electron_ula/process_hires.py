#!env/bin/python

from __future__ import print_function
import cv2
import numpy as np
from matplotlib import pyplot as plt

print("load image")
img = cv2.imread("ElectronULA_32mm_1.5X_GX7_DxO.tif")

print("size:", img.shape)

#thresholded = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 2)
#cv2.imwrite("thresholded.tif", thresholded)

#A grid point around the top left somewhere: 653,650
left = 653.0
top = 649.0
#Bottom right: 7283,6522
right = 72830
bottom = 6522.0
#5.5px/trace
trace_width = 1323.0/8/30
trace_height = 1650.0/10/30

print("drawing a bunch of lines")
y = top
while y < bottom:
    print(y)
    cv2.line(img, (int(left), int(y)), (int(right), int(y)), (0, 0, 255))  # BGR
    y += trace_height
x = left
while x < right:
    print(x)
    cv2.line(img, (int(x), int(top)), (int(x), int(bottom)), (0, 0, 255))
    x += trace_width

print("saving")
cv2.imwrite("processed.png", img)
