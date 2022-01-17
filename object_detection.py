import cv2
import numpy as np
import math
#import matplotlib.pyplot as plt

# from send_script.shape_detection import classifyShape
# from send_script.blocks import Block, Square, Rectangle, Circle, Triangle
# from send_script.color_def import ColorDef 

from shape_detection import classifyShape
from blocks import Block, Square, Rectangle, Circle, Triangle
from color_def import ColorDef

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# IMSHOW = True

def resizeImg(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    return cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)

# @param mode is unused but was intended to allow us to efficiently switch
# between different shape detection approaches
def obj_detection(img, mode):
    SrcImage = img.copy()
    org_img = img.copy()

    SrcImage = resizeImg(SrcImage, 0.75)

    # alpha = contrast and beta = brightness. Different cases:
    # alpha 1  beta 0      --> no change  
    # 0 < alpha < 1        --> lower contrast  
    # alpha > 1            --> higher contrast  
    # -127 < beta < +127   --> good range for brightness values
    if mode == 0:
        SrcImage = cv2.addWeighted(SrcImage, 0.9, SrcImage, 0, -50)
        cv2.imwrite('contrast_bright_adjust.jpg', SrcImage)
    
    # if IMSHOW == True:
    #     cv2.imshow('Weighted', SrcImage)
    #     cv2.waitKey()

    height, width = SrcImage.shape[:2]

    SrcImage = cv2.cvtColor(SrcImage, cv2.COLOR_BGR2HSV)
    colorDef = ColorDef(SrcImage)
    masks = colorDef.getMasks()

    def getCentroidComponents():
        if imgMoments["m00"] == 0.0:
            return 0, 0
            
        x = imgMoments["m10"] / imgMoments["m00"]
        y = imgMoments["m01"] / imgMoments["m00"]
        return x, y

    def getCentralMoments():
        if imgMoments["m00"] == 0.0:
            return 0, 0, 0

        mu20 = (imgMoments['m20'] / imgMoments['m00']) - (xbar * xbar)
        mu02 = (imgMoments['m02'] / imgMoments['m00']) - (ybar * ybar)
        mu11 = (imgMoments['m11'] / imgMoments['m00']) - (xbar * ybar)
        return mu20, mu02, mu11

    def drawCentroid(img):
        cv2.circle(img, (int(xbar), int(ybar)), 3, (0, 0, 255), -1)

    def drawLine(img):
        length = math.pow(height, 2) + math.pow(width, 2)
        xstart, ystart = int(xbar), int(ybar)

        xend = int(xbar + length * math.cos(principalAngle))
        yend = int(ybar + length * math.sin(principalAngle))
        cv2.line(img, (xstart, ystart), (xend, yend), WHITE, 1)

        xend = int(xbar + length * (math.cos(principalAngle) * -1))
        yend = int(ybar + length * (math.sin(principalAngle) * -1))
        cv2.line(img, (xstart, ystart), (xend, yend), WHITE, 1)

    objects = []
    count = 0

    x_coords = []
    y_coords = []
    angles = []

    for mask, color in masks:
        # if IMSHOW == True:
        #     cv2.imshow('test', np.hstack([SrcImage, cv2.bitwise_and(SrcImage, SrcImage, mask = mask)]))
        #     cv2.imwrite(color + '_mask.jpg', np.hstack([SrcImage, cv2.bitwise_and(SrcImage, SrcImage, mask = mask)]))
        #     cv2.waitKey()
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        shape_dict = {
            'RECTANGLE': Rectangle,
            'CIRCLE': Circle,
            'SQUARE': Square,
            'TRIANGLE': Triangle
        }
        for contour in contours:
            area = cv2.contourArea(contour)
            if(area > 300):
                count += 1
                shape = classifyShape(contour)
                
                x, y, w, h = cv2.boundingRect(contour)
                cv2.putText(SrcImage, str(count) + ': ' + color + ' ' + shape, (x + 25, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE)
            
                if shape != 'UNDEFINED SHAPE':
                    imgMoments = cv2.moments(contour)
                    xbar, ybar = getCentroidComponents()
                    mu20, mu02, mu11 = getCentralMoments()
                    
                    principalAngle = 0.5 * math.atan2(2 * mu11, mu20 - mu02)

                    if shape != 'UNDEFINED SHAPE':
                        objects.append(shape_dict[shape](color, shape, (xbar, ybar), principalAngle))
                            
                        x_coords.append(xbar)
                        y_coords.append(ybar)
                        angles.append(principalAngle)

                    drawCentroid(SrcImage)
                    drawLine(SrcImage)

    # if IMSHOW == True:
    #     cv2.imshow('img', cv2.cvtColor(SrcImage, cv2.COLOR_HSV2BGR))
    #     cv2.imwrite('out.jpg', cv2.cvtColor(SrcImage, cv2.COLOR_HSV2BGR))
    #     cv2.waitKey()

    return SrcImage, x_coords, y_coords, objects