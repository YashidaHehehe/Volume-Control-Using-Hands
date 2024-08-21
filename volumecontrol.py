import handtrackingmodule as h
import cv2
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)


#volume.GetMute()
volRange=volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
print(minVol,maxVol)



# #(-63.00390625, -0.00390625, 0.0625)


width_cam , height_cam = 1280,720
cap = cv2.VideoCapture(0)
cap.set(3, width_cam)
cap.set(4, height_cam)
pTime=0

detector = h.handDetector(detectionCon=0.8)



while True:
    success, img = cap.read()
    detector.findHands(img,draw = False)
    Lmlist = detector.findPos(img, draw=True)
    #print(Lmlist)
    if len(Lmlist) != 0:
        #print(Lmlist[4], Lmlist[8])
        
        x1,y1 = Lmlist[4][1],Lmlist[4][2]
        x2,y2 = Lmlist[8][1],Lmlist[8][2]
        #print(x2,y2,x1,y1)
        cx,cy = (x1+x2) //2 , (y1+y2) //2 
        #cv2.circle(img, (x1,y1),10,(255,0,255), cv2.FILLED)
        #cv2.circle(img, (x2,y2),10,(255,0,255), cv2.FILLED)
        #qcv2.line(img, (x1,y1), (x2,y2),(255,0,0),5,)
        #cv2.circle(img, (cx,cy), 7, (255,0,0), cv2.FILLED)
        
        length = math.hypot(x2-x1, y2-y1)
        print(length)
        #185 - 8 set accordingly
        
        vol = np.interp(length, [8,185], [minVol,maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
             #cv2.circle(img, (cx,cy), 7, (0,255,0), cv2.FILLED)
             print("OFF")
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

