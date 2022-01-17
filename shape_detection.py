import cv2
import numpy as np
import matplotlib.pyplot as plt

def classifyShape(blob):
    perimeter = cv2.arcLength(blob, True)
    vertices = cv2.approxPolyDP(blob, 0.01 * perimeter, True)
    print(len(vertices))

    if len(vertices) == 3:
        return "TRIANGLE"
    
    elif len(vertices) >= 4 and len(vertices) <= 8:
        centroid, (width, height), angle = cv2.minAreaRect(vertices)
        ratio = width / float(height)

        if ratio >= 0.80 and ratio <= 1.20:
            return "SQUARE" if cv2.contourArea(blob) < 3000 else "TRIANGLE"
        
        elif (ratio > 1.20 and ratio < 1.70) or (ratio < 0.80 and ratio > 0.55):
            return "TRIANGLE"
        
        else:
            return "RECTANGLE"

    elif len(vertices) > 8:
        return "CIRCLE"
    
    else:
        return "UNDEFINED SHAPE"
