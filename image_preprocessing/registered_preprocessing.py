#!/usr/bin/python
import cv2
import numpy as np
import os
import sys
from pathlib import Path


def registered_preprocessing(impath, save_path):
    # path creation reference: https://stackoverflow.com/a/41146954
    path = Path(save_path)
    path.mkdir(parents=True, exist_ok=True)
    if not(impath.endswith("/")):
        impath += "/"
    if not(save_path.endswith("/")):
        save_path += "/"

    dir_list = os.listdir(impath)
    for i in dir_list:
        if i.endswith(".png"):
            image = cv2.imread(impath + i)
            cropped = crop_boundary(image)
            if cropped is None:
                continue  # failed to crop due to the negative boundary
            cv2.imwrite(save_path + i, cropped)


def crop_boundary(image):
    output = image.copy()
    # numpy argmin/argmax reference: https://stackoverflow.com/a/51055927
    output = output[125: 985 + 1, 98: 1040 + 1]
    return output


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:\n\t python registered_preprocessing.py <imread_path> <imsave_path>")
    else:
        registered_preprocessing(sys.argv[1], sys.argv[2])
