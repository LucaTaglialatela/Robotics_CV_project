#!/usr/bin/env python
import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge
import cv2

import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
from tm_msgs.msg import *
from tm_msgs.srv import *

from sensor_msgs.msg import Image

import numpy as np
import math
import matplotlib.pyplot as plt

from send_script.object_detection import obj_detection
from send_script.template_scanner import TemplateScanner

X_RATIO, Y_RATIO = 2.2172487009228301, -2.2242599548009512
ARM_RATIO = np.array([X_RATIO, Y_RATIO])
X_BASE_PX = 629.5378878678919
Y_BASE_PX = 702.962791317086
X_BASE_MM = 350.
Y_BASE_MM = 350.

X_TARGET_MM = 700
Y_TARGET_MM = 200
Z_TARGET_MM = 112

correction = 0
last_z = 0

ROTATION_MATRIX = np.array([[np.cos(np.pi/4), -np.sin(np.pi/4)],
                            [np.sin(np.pi/4), np.cos(np.pi/4)]])

class Target:
    def __init__(self, shape, color, target_pos, target_view):
        self.shape = shape
        self.color = color
        self.target_pos = target_pos
        self.target_view = target_view



class ImageSub(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.subscription = self.create_subscription(Image, 'techman_image', self.image_callback, 10)
        self.br = CvBridge()

    def image_callback(self, data):
        self.get_logger().info('Received image')
        
        current_frame = self.br.imgmsg_to_cv2(data)

        # Save copy of unprocessed workspace
        cv2.imwrite("original.jpg", current_frame)

        current_frame, x,y,  src_objects = obj_detection(current_frame, 0)
    
        # Save copy of processed workspace
        cv2.imwrite("processed.jpg", current_frame)
        
        input('continue ?')

        scanner = TemplateScanner()
        target_list = scanner.scan()
        x = []
        y = []
        angles = []
        blockTypes = []

        target_x = []
        target_y = []
        target_orientation = []

        for i in range(len(target_list)):
            print(target_list[i])
            target_color = target_list[i].color
            target_shape = target_list[i].shape
            find = False
            for obj in src_objects:
                obj.printBlock()
                if obj.color == target_color and obj.shape == target_shape:
                    x.append(obj.getX())
                    y.append(obj.getY())
                    angles.append(obj.orientation)
                    blockTypes.append(obj.shape)

                    target_x.append(target_list[i].target_img_pos[0])
                    target_y.append(target_list[i].target_img_pos[1])
                    target_orientation.append(0)
                    src_objects.remove(obj)
                    find = True
                    break
            if not find:
                print("I cannot find the target, please give out different template")
                exit(0)

        for idx, (x_now, y_now, t_now, blockType) in enumerate(zip(x, y, angles, blockTypes)):
            
            new_angle = 360 - (math.degrees(t_now) - 45)

            pos = np.array([x_now - X_BASE_PX, y_now - Y_BASE_PX])
            new_pos = ROTATION_MATRIX@pos.T
            
            move_dir = new_pos / ARM_RATIO
            target_pos = [target_x[idx], target_y[idx]]
            
            self.moveBlock(move_dir, new_angle, target_pos, blockType)
       
        # ===================================================================================
    
    def moveBlock(self, move_dir, angle, target_pos, blockType):
            global last_z
            global correction
            
            if blockType == "CIRCLE" and abs(target_pos[1] - last_z) > 15:
                correction =-12
            last_z = target_pos[1]

            def conversion(x):
                return x * 0.5

            set_io(0.)
            
            targetP1 = "%.2f, %.2f, 200, -180.00, 0.0, %.2f" %(X_BASE_MM + move_dir[0], Y_BASE_MM + move_dir[1], angle)
            send_script("PTP(\"CPP\"," + targetP1 + ",100,200,0,false)")

            set_io(0.)

            targetP1 = "%.2f, %.2f, 116, -180.00, 0.0, %.2f" %(X_BASE_MM + move_dir[0], Y_BASE_MM + move_dir[1], angle)
            send_script("PTP(\"CPP\"," + targetP1 + ",100,200,0,false)")
        
            set_io(1.)

            targetP1 = "%.2f, %.2f, 300.0, -180.0, 0.0, 135.0" %(X_BASE_MM + move_dir[0], Y_BASE_MM + move_dir[1])
            send_script("PTP(\"CPP\"," + targetP1 + ",100,200,0,false)")

            x_new = conversion(target_pos[0])
            y_new = Y_TARGET_MM

            target_pos[1] = conversion(target_pos[1])

            targetP1 = "%.2f, %.2f, 300.0, -180.0, 0.0, 90.0" %(X_TARGET_MM + x_new, y_new )
            send_script("PTP(\"CPP\"," + targetP1 + ",100,200,0,false)")
            
            targetP1 = "%.2f, %.2f, %.2f, -180.0, 0.0, 90.0" %(X_TARGET_MM + x_new, y_new, Z_TARGET_MM+target_pos[1]+correction)
            send_script("PTP(\"CPP\"," + targetP1 + ",100,200,0,false)")

            set_io(0.)

            targetP1 = "%.2f, %.2f, 300.0, -180.0, 0.0, 90.0" %(X_TARGET_MM + x_new, y_new)
            send_script("PTP(\"CPP\"," + targetP1 + ",100,200,0,false)")
            

def send_script(script):
    arm_node = rclpy.create_node('arm')
    arm_cli = arm_node.create_client(SendScript, 'send_script')

    while not arm_cli.wait_for_service(timeout_sec=1.0):
        arm_node.get_logger().info('service not availabe, waiting again...')

    move_cmd = SendScript.Request()
    move_cmd.script = script
    arm_cli.call_async(move_cmd)
    arm_node.destroy_node()

def set_io(state):
    gripper_node = rclpy.create_node('gripper')
    gripper_cli = gripper_node.create_client(SetIO, 'set_io')

    while not gripper_cli.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('service not availabe, waiting again...')

    io_cmd = SetIO.Request()
    io_cmd.module = 1
    io_cmd.type = 1
    io_cmd.pin = 0
    io_cmd.state = state
    gripper_cli.call_async(io_cmd)
    gripper_node.destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ImageSub('image_sub')
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
