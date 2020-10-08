from cv2 import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import os

folder = "saved"

if os.path.isdir(folder)==False:
    print(os.path.isdir(folder))
    os.mkdir(folder)

cap = cv2.VideoCapture(1)

addMargin = 0

while True:
    success, img = cap.read()
    #print(img.shape)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    for barcode in decode(imgGray):
        (x, y, w, h) = barcode.rect
        #if y-addMargin<0: y=addMargin
        #if y+h+addMargin>
        #if x-addMargin<0: x=addMargin
        #if x+w+addMargin>
        #print(str(x),"-",str(x+w+addMargin),"-",str(img.shape[1]))
        #print(str(x),"-",str(x+w+addMargin),"-",str(y),"-",str(y+h+addMargin))
        codeData = barcode.data.decode("utf-8")
        procDay=str(time.localtime()[2])+"/"+str(time.localtime()[1])+"/"+str(time.localtime()[0])
        procHour=str(time.localtime()[3])+":"+str(time.localtime()[4])+":"+str(time.localtime()[5])
        #print(codeData,procDay,procHour,sep=" - ")
        croppedImg = img[y-addMargin:y+h+addMargin,x-addMargin:x+w+addMargin]
        scaledImg = cv2.resize(croppedImg,(croppedImg.shape[1]*5,croppedImg.shape[0]*5))
        #cv2.imshow("Cropped",croppedImg)
        cv2.rectangle(scaledImg, (0, 0), (scaledImg.shape[1], scaledImg.shape[0]), (255, 0, 0), 2) 
        cv2.putText(scaledImg,procDay+"-"+procHour,(10,10),cv2.FONT_HERSHEY_TRIPLEX,1,(0,230,0),1)
        cv2.putText(scaledImg,codeData,(10,40),cv2.FONT_HERSHEY_TRIPLEX,1,(0,230,0),1)     
        cv2.imshow("Cropped",scaledImg)
        cv2.rectangle(img, (x - addMargin, y - addMargin), (x + w + addMargin, y + h + addMargin), (255, 0, 0), 2)

    cv2.imshow("Video",img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
