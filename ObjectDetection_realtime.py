from typing import Any
import cv2
import numpy as np
import pandas as pd
import matplotlib
import torch
import yaml
import time
from PIL import Image

LOG_CURR = 1
EPS = 3
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
#BGR color format
COLOR = (0, 0, 255)
THICKNESS = 1

class Object_Detection:
    
    #Variable
    device=None
    model=None
    
    def __init__(self,dev='0'):
        if (torch.cuda.is_available() and dev!='cpu'):  
            self.device = dev
        else:
            if (dev!='cpu'):
                global log
                global cnt
                log.write("{} GPU is not available change to CPU".format(cnt))
            self.device = 'cpu'
        
    def load_model(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./YOLO_model/yolov5m_Objects365.pt')
        if (self.device=='cpu'):
            self.model.cpu()
        else:
            self.model.cuda()
        self.model.max_det = 10
        
    def score_frame(self,frame):
        frame = [frame]
        results = self.model(frame)
        return results.pandas().xyxy
        
    def draw_box(self,frame,res,isRunning=False):
        if not isRunning:
            return frame
        #Draw bounding box to frame
        for idx in res:
            #idx.sort_values('xmin','ymin')
            info2 =idx.to_dict(orient = "records")
            if len(info2) != 0:
                for result in info2:
                    name = result['name']
                    x1 = round(result['xmin'])
                    x2 = round(result['xmax'])
                    y1 = round(result['ymin'])
                    y2 = round(result['ymax'])
                    confidence = str(result['confidence'])
                    global EPS
                    global FONT
                    global FONT_SCALE
                    global COLOR
                    global THICKNESS
                    cv2.rectangle(frame, (x1,y2), (x2,y1), COLOR, THICKNESS)
                    cv2.putText(frame, name, (x1-EPS,y2-EPS), FONT, FONT_SCALE, (0,255,0), THICKNESS, cv2.LINE_AA)
                    cv2.putText(frame, confidence, (x2-EPS,y1-EPS), FONT, FONT_SCALE, (255,0,0), THICKNESS, cv2.LINE_AA)
            else:
                break
        return frame
    
    def get_data(self,res,isRunning=False):
        data = []
        if not isRunning:
            return data
        #Confidence > 0.3 (30%) -> add to data
        for idx in res:
            info2 =idx.to_dict(orient = "records")
            if len(info2) != 0:
                for result in info2:
                    name = str(result['name'])
                    confidence = float(result['confidence'])
                    if (confidence > 0.3):
                        data.append(name)
            else:
                break
        return data
    
    def img_detect(self, res):
        return self.get_data(res,True)
    
    def get_closest(self, img):
        self.load_model()
        results = self.model(img)
        #results.show()
        res = results.pandas().xyxy
        maxconfidence = 0.0
        answer = ""
        #Confidence > 0.35 (35%) -> add to data
        for idx in res:
            info2 =idx.to_dict(orient = "records")
            if len(info2) != 0:
                for result in info2:
                    x1 = result['xmin']
                    x2 = result['xmax']
                    y1 = result['ymin']
                    y2 = result['ymax']
                    name = str(result['name'])
                    confidence = float(result['confidence'])
                    
                    if (confidence <= 0.35):
                        continue
                    if (confidence > maxconfidence):
                        maxconfidence = confidence
                        answer = name
            else:
                break
        return str(answer)
    
    def detect(self):
        self.load_model()
        capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        
        if not capture.isOpened():
            return

        while (True):
            ret,frame = capture.read()   
            if ret == True:
                res = self.score_frame(frame)
                show_frame = self.draw_box(frame,res,True)
                cv2.imshow('Detection', np.squeeze(show_frame))
                global data
                #print(data[label])
            
            #Break when failing to capture
            if ret == False:
                break
            
            #Break key
            if cv2.waitKey(500) & 0xFF == ord('q'):
                exit(0)
                break
            # if 0xFF == ord('q'):
            #     break
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def list_objects(self,img):
        self.load_model()
        results = self.model(img)
        res = results.pandas().xyxy
        DATA = self.img_detect(res)
        objects = open("./logs/objects_res.txt","w")
        for i in DATA:
            objects.write(i + '\n')
            
    def __call__(self):
        self.load_model()
    
data = None

def LoadData():
    with open("./logs/object_list.yaml","r") as yml:
        data = yaml.load(yml, Loader=yaml.FullLoader)
    log = open("./logs/log.txt","w")

Object = Object_Detection("0")

# Image
#img = Image.open('./Images/coffee.jpg')

#Object.list_objects(img)
Object.detect()