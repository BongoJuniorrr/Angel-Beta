import cv2
import pytesseract
from PIL import Image,ImageEnhance
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

video = cv2.VideoCapture("TextScanning_Ads.mp4")
frame_width = int(video.get(3)) 
frame_height = int(video.get(4))
size = (frame_width, frame_height) 
result = cv2.VideoWriter('TextScanning_Result.avi', 
						cv2.VideoWriter_fourcc(*'DIVX'), 
						60, size) 
d=0
while True:
    ret,frame = video.read()
    if ret==True:
        #characters
        ans = ""
        hImg,wImg,_ = frame.shape
        boxes = pytesseract.image_to_data(frame)
        #print(boxes)
        for x,b in enumerate(boxes.splitlines()):
            if x!=0:
                b = b.split()
                if len(b) == 12:
                    x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                    cv2.rectangle(frame,(x,y),(w+x,h+y),(0,0,255),3)
                    cv2.putText(frame,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
                    if (b[11] == '|'):
                        b[11]='I'
                    ans = ans + b[11] + ' '
        result.write(frame)
        d+=1
        print(d)
    else:
        break
                
video.release() 
result.release() 
cv2.destroyAllWindows()
print("Finished!")