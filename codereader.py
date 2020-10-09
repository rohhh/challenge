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

registeredCodes = []
count = 0

while True:

    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  

    for barcode in decode(imgGray):
        t=time.time()
        procDay=str(time.localtime()[2])+"/"+str(time.localtime()[1])+"/"+str(time.localtime()[0])
        procHour=str(time.localtime()[3])+":"+str(time.localtime()[4])+":"+str(time.localtime()[5])
        
        addMarginT = 40
        addMarginL = 40
        addMarginR = 40
        addMarginB = 40
        scale = 5
        pointsList = []

        (x, y, w, h) = barcode.rect
        barType=barcode.type
        pointsList = barcode.polygon
        codeData = barcode.data.decode("utf-8")

        if y-addMarginT<0: addMarginT=0 
        if y+h+addMarginB>img.shape[0]: addMarginB=0
        if x-addMarginL<0: addMarginL=0
        if x+w+addMarginR>img.shape[1]: addMarginR=0
        
        croppedImg = img[y-addMarginT:y+h+addMarginB,x-addMarginL:x+w+addMarginR]
        if croppedImg.shape[0]*croppedImg.shape[1]>0:
            scaledImg = cv2.resize(croppedImg,(croppedImg.shape[1]*scale,croppedImg.shape[0]*scale))
            if barType=="QRCODE":
                for i in range(len(pointsList)):
                    cv2.line(img, pointsList[i], pointsList[i-1], (255, 0, 0), 2)
                    cv2.line(scaledImg, ((pointsList[i][0]-x+addMarginL)*scale,(pointsList[i][1]-y+addMarginT)*scale), ((pointsList[i-1][0]-x+addMarginL)*scale,(pointsList[i-1][1]-y+addMarginT)*scale), (255, 0, 0), 2)     
            else:
                for i in range(len(pointsList)):
                    cv2.line(img, pointsList[i], pointsList[i-1], (0, 125, 255), 1)
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.rectangle(scaledImg, (addMarginL*scale, addMarginT*scale), ((addMarginL + w)*scale, (addMarginT + h)*scale), (255, 0, 0), 2)

            if codeData not in registeredCodes:
                registeredCodes.append(codeData)
                count += 1
                cv2.putText(scaledImg,procDay+"-"+procHour,(10,25),cv2.FONT_HERSHEY_TRIPLEX,0.6,(225,0,0),1)
                cv2.putText(scaledImg,barType+" : "+codeData,(10,50),cv2.FONT_HERSHEY_TRIPLEX,0.6,(225,0,0),1)
                cv2.putText(scaledImg,"Processing time : "+str(round((time.time()-t)*1000,3))+"ms",(10,75),cv2.FONT_HERSHEY_TRIPLEX,0.6,(225,0,0),1)
                print(str(count)+" saved code(s): "+codeData)
                cv2.imwrite("saved/code"+str(count)+".jpg",scaledImg)
            else:
                cv2.putText(img,"Code"+str(registeredCodes.index(codeData)+1)+".jpg",(x,y),cv2.FONT_HERSHEY_PLAIN,1.7,(10,120,0),2)
                
            
    cv2.putText(img,str(count)+" registered codes.",(10,25),cv2.FONT_HERSHEY_TRIPLEX,0.5,(125,0,0),1)
    cv2.imshow("Codes",img)
    #cv2.imshow("Codes gray",imgGray)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
