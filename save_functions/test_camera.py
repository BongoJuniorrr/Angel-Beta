import cv2

cam = cv2.VideoCapture(1,cv2.CAP_DSHOW)
res, frame = cam.read()
cv2.imshow("IMG", frame)
cv2.waitKey(0)