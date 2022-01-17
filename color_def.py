import cv2
import numpy as np

class ColorDef:
    def __init__(self, img):
        self.img = img

    def processMask(self, mask):
        eroded = cv2.erode(mask, (5, 5), iterations = 5)
        return eroded

    def getRedMask(self):
        red_lower = np.array([0, 50, 70], dtype = "uint8")
        red_upper = np.array([20, 255, 255], dtype = "uint8")
        red_mask = cv2.inRange(self.img, red_lower, red_upper)
        return self.processMask(red_mask)

    def getBlueMask(self):
        blue_lower = np.array([80, 20, 60], dtype = "uint8")
        blue_upper = np.array([135, 255, 255], dtype = "uint8")
        blue_mask = cv2.inRange(self.img, blue_lower, blue_upper)
        return self.processMask(blue_mask)

    def getGreenMask(self):
        green_lower = np.array([32, 20, 60], dtype = "uint8")
        green_upper = np.array([85, 255, 255], dtype = "uint8")
        green_mask = cv2.inRange(self.img, green_lower, green_upper)
        return self.processMask(green_mask)

    def getYellowMask(self):
        yellow_lower = np.array([18, 20, 115], dtype = "uint8")
        yellow_upper = np.array([36, 255, 255], dtype = "uint8")
        yellow_mask = cv2.inRange(self.img, yellow_lower, yellow_upper)
        return self.processMask(yellow_mask)

    def getMasks(self):
        return [
                (self.getRedMask(), 'RED'),
                (self.getBlueMask(), 'BLUE'),
                (self.getGreenMask(), 'GREEN'),
                (self.getYellowMask(), 'YELLOW')
               ]