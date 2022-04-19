import numpy as np
import math
import cv2
import math
import lpips
import torch
from PIL import Image
import torchvision.transforms.functional as TF
from numba import jit


def mse(img1, img2):
    mse = np.mean(np.subtract(img1, img2) ** 2)
    return mse

def sq_err(img1, img2):
    return np.sum(np.subtract(img1, img2))

# reference: https://dsp.stackexchange.com/a/50704
def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

# https://cvnote.ddlee.cc/2019/09/12/psnr-ssim-python
def ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()


def calculate_ssim(img1, img2):
    '''calculate SSIM
    the same outputs as MATLAB's
    img1, img2: [0, 255]
    '''
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1, img2))
            return np.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')

@jit
def pixel_brightness(pixel):
    '''
    brightness = sqrt(0.299 * R^2 + 0.587 * G^2 + 0.114 * B^2)
    Input: each pixel from image
    Output: computation result indicated above
    '''
    assert 3 == len(pixel)
    r, g, b = pixel
    return math.sqrt(0.299 * r ** 2 + 0.587 * g ** 2 + 0.114 * b ** 2)

@jit
def image_brightness(img):
    '''
    Calculates brightness, return the brightness value per single image
    Input: single image read with opencv2
    Output: calculated brightness value
    '''
    nr_of_pixels = len(img) * len(img[0])

    sum_brightness = 0
    for row in img:
        for pixel in row:
            sum_brightness += pixel_brightness(pixel)

    return sum_brightness / nr_of_pixels

@jit
def sqrt_transform(img):
    '''
    Apply square root transform to the given image
    Input: single image read with opencv2
    Output: sqrt transform applied image
    '''
    h = img.shape[0]
    w = img.shape[1]
    for y in range(0, h):
        for x in range(0, w):
            img[y, x] = np.sqrt(img[y, x])
    
    sqrt_img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    return sqrt_img