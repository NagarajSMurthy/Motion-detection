#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 2 16:35:03 2019

@author: nagaraj
"""

from single_motiondetector import SingleMotionDetector
import cv2
#import time
import datetime

capture = cv2.VideoCapture(0)
md = SingleMotionDetector(accumWeight = 0.4)
total = 0            # total number of frames read so far
frameCount = 16
thresh = None

while True:
    ret, frame = capture.read()
    if ret == False:
        continue
        
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (400, 600))
    original_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(7,7), 0)
    timestamp = datetime.datetime.now()
    cv2.putText(frame, timestamp.strftime(
        "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    # We had sufficient frames for building background model. Now, we are detecting any motion present
    # Initially total = 0, the control directly skips this if condition and creates a background model
    if total > frameCount:
        # detect motion in the image
        motion = md.detect(gray)

	# check to see if motion was found in the frame
        if motion is not None:
            # unpack the tuple and draw the box surrounding the
	        # "motion area" on the output frame
            (thresh, (minX, minY, maxX, maxY)) = motion
            cv2.rectangle(frame, (minX, minY), (maxX, maxY),(0, 0, 255), 2)
		
    # update the background model and increment the total number of frames read so far
    # if total > framecount, we detect the motion with the available background
    # model and the update the model. Else, we first build the background model.
        
    md.update(gray)
    total += 1
    outputFrame = frame.copy()
    if thresh is not None:
        cv2.imshow('What I see',thresh)

    cv2.imshow('Original',original_frame)
    cv2.imshow('Motion detected frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        capture.release()
        cv2.destroyAllWindows()
