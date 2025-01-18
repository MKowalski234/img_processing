import cv2 as cv
import numpy as np

def canny(image):
    return cv.Canny(image, 125, 175)

def invert(image):
    return 255 - image

def gray(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def adjust_saturation(image, factor):
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV).astype(np.float32)
    hsv_image[..., 1] *= factor
    hsv_image[..., 1] = np.clip(hsv_image[..., 1], 0, 255)
    return cv.cvtColor(hsv_image.astype(np.uint8), cv.COLOR_HSV2BGR)
