from skimage import io
import joblib
import os
import sys
import time
import serial
global url
import numpy
import cv2
url="http://192.168.0.103:8080/shot.jpg"
s=serial.Serial('COM6',9600)
time.sleep(2)

alg=joblib.load('mymodel.pkl')
#scaler=joblib.load('scalermodel.pkl')
print('model loaded')

def drive():
    img=io.imread(url)
    cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img=cv2.blur(img,(5,5))
    retval,img=cv2.threshold(img,210,255,cv2.THRESH_BINARY)
    img=cv2.resize(img,(24,24))
    retval,img=cv2.threshold(img,210,255,cv2.THRESH_BINARY)
    image_as_array=numpy.ndarray.flatten(numpy.array(img))
    #image_as_array=scaler.transform(image_as_array)
    result=alg.predict([image_as_array])[0]
    if result=='f':
        s.write(b'f')
        time.sleep(1)
    elif result=='r':
        s.write(b'r')
        time.sleep(1)
    elif result=='l':
        s.write(b'l')
        time.sleep(1)
    time.sleep(1)
    print(result)
    drive()
print("Start Driving")
try:
    drive()

except(KeyboardInterrupt):
    print('Stopping drive')
    s.close()

s.close()
