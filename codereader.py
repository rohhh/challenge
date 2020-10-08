from cv2 import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import os

cap = cv2.VideoCapture(1)
#cap.release
#imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

while True:
    success, img = cap.read()
    for barcode in decode(img):
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        codeData = barcode.data.decode("utf-8")
        print(codeData)
    cv2.imshow("Video",img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
