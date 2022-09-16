import cv2, time
import imutils
import numpy as np
from numpy.core import umath



first_frame=None
video=cv2.VideoCapture(0)

def Track(x):
    pass

cv2.namedWindow("Select Color")
cv2.createTrackbar("uh", "Select Color", 153, 180, Track)
cv2.createTrackbar("us", "Select Color", 255, 255, Track)
cv2.createTrackbar("uv", "Select Color", 255, 255, Track)
cv2.createTrackbar("lh", "Select Color", 62, 180, Track)
cv2.createTrackbar("ls", "Select Color", 74, 255, Track)
cv2.createTrackbar("lv", "Select Color", 49, 255, Track)

tpl=(0,0)

sheet=None

def changecolor(center):

    return (255,215,0)


while True:
    check, frame=video.read()
    frame=cv2.flip(frame,1)
    value=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel=np.ones((5,5),np.uint8)
    

    uh=cv2.getTrackbarPos("uh", "Select Color")
    us=cv2.getTrackbarPos("us", "Select Color")
    uv=cv2.getTrackbarPos("uv", "Select Color")
    lh=cv2.getTrackbarPos("lh", "Select Color")
    ls=cv2.getTrackbarPos("ls", "Select Color")
    lv=cv2.getTrackbarPos("lv", "Select Color") 
    
    
    ublack=np.array([uh, us, uv])
    lblack=np.array([lh, ls, lv])

    thresh=cv2.inRange(value, lblack, ublack)
    vari=cv2.bitwise_and(frame, frame, mask=thresh)
    vari=cv2.dilate(thresh, kernel, iterations=1)

    
    thresh=cv2.erode(thresh, kernel, iterations=1)
    thresh=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh=cv2.dilate(thresh, kernel, iterations=1)

    if sheet is None:
        sheet=np.ones(frame.shape)

    

    contour,_=cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contour)>0:
        count=sorted(contour, key=cv2.contourArea, reverse=True)[0]
        (x, y), r=cv2.minEnclosingCircle(count)
        cv2.circle(frame, (int(x), int(y)), int(r), (128,0,128), 2)
        move=cv2.moments(count)
        # center=(move['m10']/move['m00'], move['m01']/move['m00'])
        center=(int(move['m10']/move['m00']), int(move['m01']/move['m00']))
        #global tpl
        if tpl==(0,0):
            tpl=center
        else:    
            cg=changecolor(center)
            frame=cv2.line(frame, tpl, center, cg, 3)
            
            sheet=cv2.line(sheet, tpl, center, cg, 3)

        tpl=center    
    else:
        tpl=(0,0)    
    

    #print(center)
    sheet=cv2.rectangle(sheet, (40,1), (140,65), (0,255,0), -1)
    sheet=cv2.rectangle(sheet, (150,1), (255,65), (255,255,0), -1)
    sheet=cv2.rectangle(sheet, (275,1), (370,65), (255,0,0), -1)
    sheet=cv2.rectangle(sheet, (390,1), (485,65), (0,0,128), -1)
    
   
    
    #frame=imutils.resize(frame,width=700)
    frame=cv2.resize(frame, (640, 380))
    vari=imutils.resize(vari,width=700)



    cv2.imshow("Capturing",sheet)
    cv2.imshow("Color",vari)
    cv2.imshow("Cam",frame)
    
    if cv2.waitKey(1)==ord('g'):
        break

 

video.release()

cv2.destroyAllWindows()