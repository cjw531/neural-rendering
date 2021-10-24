#!/usr/bin/python
import cv2
import numpy as np
import os
import sys
from pathlib import Path

def hologram_preprocessing(impath, save_path):
    # path creation reference: https://stackoverflow.com/a/41146954
    path = Path(save_path)
    path.mkdir(parents=True, exist_ok=True)
    if not(impath.endswith("/")): impath += "/"
    if not(save_path.endswith("/")): save_path += "/"

    dir_list = os.listdir(impath)
    for i in dir_list:
        if i.endswith(".png"):
            image = cv2.imread(impath + i)
            circles = detect_circles(image)
            if circles is None: continue # no circle detected
            num_marker, output, circlesRound = detect_markers(circles, image)
            if num_marker != 6: continue # all 6 markers should be detected
            cropped = crop_boundary(output, circlesRound)
            if cropped is None: continue # failed to crop due to the negative boundary
            rotated = rotate_img(cropped)
            cv2.imwrite(save_path + i, rotated)

def detect_circles(image):
    height, width = image.shape[:2]
    maxRadius = int(1.1 * (width / 100) / 2)  # hardcoded
    minRadius = int(0.9 * (width / 140) / 2)  # hardcoded

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(image=gray,
                               method=cv2.HOUGH_GRADIENT,
                               dp=1.2,
                               minDist=2*minRadius,
                               param1=50,
                               param2=50,
                               minRadius=minRadius,
                               maxRadius=maxRadius
                               )
    return circles

def detect_markers(circles, image):
    output = image.copy()
    # convert the (x, y) coordinates and radius of the circles to integers
    circlesRound = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circlesRound:
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.circle(output, (x, y), radius=2, color=(0, 0, 255), thickness=2)

    return len(circlesRound), output, circlesRound

def crop_boundary(image, circlesRound):
    output = image.copy()
    # numpy argmin/argmax reference: https://stackoverflow.com/a/51055927
    lower_left = np.argmax(circlesRound, axis=0)[1]
    lower_right_x = circlesRound[lower_left][0] + 920
    lower_right_y = circlesRound[lower_left][1] + 105

    upper_left = np.argmin(circlesRound, axis=0)[0]
    upper_left_x = circlesRound[lower_left][0] + 75
    upper_left_y = circlesRound[upper_left][1] - 120

    if (lower_right_x < 0) or (lower_right_y < 0) or (upper_left_x < 0) or (upper_left_y < 0):
        return None

    output = output[upper_left_y : lower_right_y + 1, upper_left_x : lower_right_x + 1]
    return output

def rotate_img(image):
    output = image.copy()
    # rotate 270 by rotating 90 by 3 times
    rotated = np.rot90(output)
    rotated = np.rot90(rotated)
    rotated = np.rot90(rotated)
    return rotated

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:\n\t python hologram_preprocessing.py <imread_path> <imsave_path>")
    else:
        hologram_preprocessing(sys.argv[1], sys.argv[2])