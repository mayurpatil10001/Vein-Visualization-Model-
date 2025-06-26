#!/usr/bin/python3
import cv2
import numpy as np
import time
from picamera2 import Picamera2

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (480, 320)}))
picam2.start()

time.sleep(2)

# Best approximate HSV range for veins using NoIR camera under IR light (adjust if needed)
hsv_lower = np.array([100, 40, 40])
hsv_upper = np.array([140, 255, 255])

# CLAHE setup
clahe = cv2.createCLAHE(clipLimit=5, tileGridSize=(12, 12))

while True:
    frame = picam2.capture_array()

    # Convert to HSV and isolate dark blue-ish regions (veins)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    masked_region = cv2.bitwise_and(frame, frame, mask=mask)

    # Extract value channel and enhance contrast
    v_channel = cv2.cvtColor(masked_region, cv2.COLOR_BGR2GRAY)
    enhanced = clahe.apply(v_channel)

    # Apply bilateral filter to reduce noise while keeping edges
    smooth = cv2.bilateralFilter(enhanced, 4, 200, 2)

    # Adaptive thresholding for vein segmentation
    thresh = cv2.adaptiveThreshold(smooth, 255, 
                                   cv2.ADAPTIVE_THRESH_MEAN_C, 
                                   cv2.THRESH_BINARY_INV, 
                                   27, 6)

    # Morphological operations to connect broken parts
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    kernel_small = np.ones((2,2), np.uint8)
    morphed = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, kernel_small)

    # Find contours and draw them on the original image
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    overlay = frame.copy()
    cv2.drawContours(overlay, contours, -1, (0, 0, 255), 1)

    # Blend the result for semi-transparent vein visualization
    output = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    # Display the output
    cv2.imshow('Vein Visualization', output)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()