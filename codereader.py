from cv2 import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import os

folder = "saved/"

if os.path.isdir(folder)==False:
    print(os.path.isdir(folder))
    os.mkdir(folder)

cap = cv2.VideoCapture(1)

while True:

    count = 0
    success, img = cap.read()
    #img2=cv2.imread("qrcodes3.jpg")
    #img=cv2.resize(img2,(640,480))   
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #print(decode(imgGray))
    
    for barcode in decode(imgGray):
        procDay=str(time.localtime()[2])+"/"+str(time.localtime()[1])+"/"+str(time.localtime()[0])
        procHour=str(time.localtime()[3])+":"+str(time.localtime()[4])+":"+str(time.localtime()[5])
        
        addMarginT = 40
        addMarginL = 40
        addMarginR = 40
        addMarginB = 40
        scale=5
        pointsList= []

        (x, y, w, h) = barcode.rect
        barType=barcode.type
        pointsList = barcode.polygon
        codeData = barcode.data.decode("utf-8")

        if y-addMarginT<0: addMarginT=0 
        if y+h+addMarginB>img.shape[0]: addMarginB=0
        if x-addMarginL<0: addMarginL=0
        if x+w+addMarginR>img.shape[1]: addMarginR=0
        
        croppedImg = img[y-addMarginT:y+h+addMarginB,x-addMarginL:x+w+addMarginR]
        scaledImg = cv2.resize(croppedImg,(croppedImg.shape[1]*scale,croppedImg.shape[0]*scale))
        if barType=="QRCODE":
            for i in range(len(pointsList)):
                cv2.line(scaledImg, ((pointsList[i][0]-x+addMarginL)*scale,(pointsList[i][1]-y+addMarginT)*scale), ((pointsList[i-1][0]-x+addMarginL)*scale,(pointsList[i-1][1]-y+addMarginT)*scale), (255, 0, 0), 2)     
        else:
            cv2.rectangle(scaledImg, (addMarginL*scale, addMarginT*scale), ((addMarginL + w)*scale, (addMarginT + h)*scale), (255, 0, 0), 2)
        cv2.putText(scaledImg,procDay+"-"+procHour,(10,25),cv2.FONT_HERSHEY_TRIPLEX,0.6,(0,230,0),1)
        cv2.putText(scaledImg,codeData,(10,50),cv2.FONT_HERSHEY_TRIPLEX,0.6,(0,230,0),1)
        cv2.putText(img,procDay+"-"+procHour,(10,25),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,230,0),1)
        cv2.putText(img,codeData,(10,45),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,230,0),1)      
        #cv2.imshow("Cropped",scaledImg)
        for i in range(len(pointsList)):
            cv2.line(img, pointsList[i], pointsList[i-1], (255, 0, 0), 2)
        cv2.imwrite("saved/code"+str(count)+".jpg",scaledImg)
        cv2.imwrite("saved/code"+str(count)+"_full.jpg",img)
        count += 1

    cv2.imshow("Codes",img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
