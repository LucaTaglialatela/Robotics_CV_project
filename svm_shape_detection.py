import cv2
import numpy as np
import pickle
import torch
import torch.nn as nn
import torchvision.models as models
from sklearn.svm import SVC
from torchvision import datasets, transforms as T
from PIL import Image

class ShapeSVM:
    def __init__(self):
        self.shape_list = ["CIRCLE", "TRIANGLE", "RECTANGLE", "SQUARE"]

        self.svm = pickle.load(open('/home/robotics/workspace2/team10_ws/src/send_script/send_script/shape_svm.pkl', 'rb'))
        self.resnet = models.resnet18(pretrained=True)
        for param in self.resnet.parameters():
            param.requires_grad = False
        self.resnet.fc = nn.Flatten()
        self.img_transform = T.Compose([T.Resize(224), T.ToTensor(), T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

    def classify(self, img, contour):
        mat = np.zeros((150, 150, 3)).astype(np.uint8)
        x,y,w,h = cv2.boundingRect(contour)

        x -= 15
        y -= 15
        w += 30
        h += 30
        crop_img = img[y:y+h, x:x+w]
        cv2.waitKey(0)
        paste_x = 75 - w//2
        paste_y = 75 - h//2
        mat[paste_y:paste_y+h, paste_x:paste_x+w] = crop_img
        cv2.imshow('tmp', crop_img)
        cv2.waitKey(0)

        img = Image.fromarray(cv2.cvtColor(mat, cv2.COLOR_BGR2RGB))
        img.show()
        img = self.img_transform(img)
        feature = self.resnet(img.unsqueeze(0))
        predict_cls = self.svm.predict(feature)
        print(self.shape_list[int(predict_cls)-1])
        return self.shape_list[int(predict_cls)-1]
