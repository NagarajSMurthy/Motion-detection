#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 2 16:35:03 2019

@author: nagaraj
"""

import numpy as np
import cv2


class SingleMotionDetector:

    def __init__(self,accumWeight = 0.5):
        self.accumWeight = accumWeight
        # Background initialization 
        self.bg = None

    def update(self,image):
        # We set the very first frame as our background model initially. 
        if self.bg is None:
            self.bg = image.copy().astype('float')
            return
        # Computing the running average of the existing previous frames(background model) and the current frame.
        cv2.accumulateWeighted(image,self.bg,self.accumWeight)

    def detect(self,image,tVal = 25):

        # Computing the difference between the background model and the current frame. 
        delta = cv2.absdiff(self.bg.astype('uint8'), image)
        # Thresholding the output of subtraction to mark each pixels as motion (White) or background (black)
        # Difference > tVal = 255
        ret, thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY) # ret is same as threshold value. It is used in Otsu binarization.
        
        # Removing small noise and other small localized areas of motion that would otherwise be considered as false positives.
        thresh = cv2.erode(thresh, None, iterations=4)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Applying contour detection to extract the changes in motion
        
        cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = imutils.grab_contours(cnts)

        # Defining the bounding box for the motion detected.
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        if len(cnts) == 0:
            return None

        for c in cnts:

            # Computing the straight rectangular bounding box and using the x,y,width and height values to update the bounding box regions.
            (x,y,w,h) = cv2.boundingRect(c) # returns (x,y) and also width & height
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x+w), max(maxY, y+h))

        return (thresh, (minX, minY, maxX, maxY))
    
    
        
