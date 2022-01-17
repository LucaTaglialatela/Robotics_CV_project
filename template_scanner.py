import cv2
import numpy as np
import math
import send_script.object_detection

from send_script.target_block import TargetBlock

class TemplateScanner:
    def __init__(self, template_path = "game_template.png"):
        self.template_path = template_path

    def scan(self):
        target_blocks = []

        img = cv2.imread(self.template_path)
        h, w = img.shape[:2]
        work_img = img.copy()
        _, _, _, objects = send_script.object_detection.obj_detection(work_img, mode = 1)
        objects.sort(key=lambda x: (x.centroid[1], x.centroid[0]), reverse=True)

        for obj in objects:
            mode = 0
            if obj.shape == "RECTANGLE":
                degree = math.degrees(obj.orientation) 
                print("degree", degree)
                tmp = img[int(obj.centroid[1])-20:int(obj.centroid[1])+20, 
                          int(obj.centroid[0])-20:int(obj.centroid[0])+20]
                if degree > 85 and degree < 95:
                    obj.shape = "CIRCLE"
                    obj.mode = 0
           
            new_x = obj.centroid[0] - w/2
            new_y = h - obj.centroid[1]
            t_b = TargetBlock(obj.color, obj.shape, (new_x, new_y), mode = mode)
            target_blocks.append(t_b)

        for obj in objects:
            obj.printBlock()

        return target_blocks

t = TemplateScanner().scan()