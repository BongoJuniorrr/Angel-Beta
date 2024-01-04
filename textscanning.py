import cv2
import pytesseract
from PIL import Image,ImageEnhance

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def run():
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    res, frame = cam.read()

    # #frame = cv2.flip(frame, 2)
    cv2.imwrite("./Images/TEXT.png", frame)
    img = Image.open('./Images/TEXT.png')
    pixels = img.load()
    new_img = Image.new(img.mode, img.size)
    pixels_new = new_img.load()
    for i in range(new_img.size[0]):
        for j in range(new_img.size[1]):
            r, b, g = pixels[i,j]
            avg = int(round((r + b + g) / 3))
            pixels_new[i,j] = (avg, avg, avg, 0)
    # res, frame = cam.read()
    # img = cv2.imread('Images/TEXT.png')
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    enhancer = ImageEnhance.Contrast(new_img)
    new_img = enhancer.enhance(2.0)
    # Or save it to file
    # new_img.save('rick-morty-%s.png' % i)
    new_img.save("./Images/TEXT2.png")
    img = cv2.imread("./Images/TEXT2.png")
    #characters
    ans = ""
    hImg,wImg,_ = img.shape
    boxes = pytesseract.image_to_data(img)
    #print(boxes)
    for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b) == 12:
                x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                #cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),3)
                cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
                if (b[11] == '|'):
                    b[11]='I'
                ans = ans + b[11] + ' ' 
    #OUT
    fi = open("./logs/text_log.txt","w")
    fi.write(ans)
    fi.close()
