import cv2 
import numpy as np 
from collections import deque
import pyautogui 
def nothing(x):
    print(x)

buffer = 20

#Points deque structure storing 'buffer' no. of object coordinates
pts = deque(maxlen = buffer)
(dX, dY) = (0, 0)
counter = 0
direction = ''
#so i will be able to use different color for the stick
'''
cv2.namedWindow("Tracking")
#making trackbar (horizontal slider)
cv2.createTrackbar('LH',"Tracking",0,360,nothing)
cv2.createTrackbar('LS',"Tracking",0,360,nothing)
cv2.createTrackbar('LV',"Tracking",0,360,nothing)
cv2.createTrackbar('UH',"Tracking",255,255,nothing)
cv2.createTrackbar('US',"Tracking",255,255,nothing)
cv2.createTrackbar('UV',"Tracking",255,255,nothing)
'''
#making a window 
cv2.namedWindow("Image")
#opening the webcam
cap=cv2.VideoCapture(0)
#reading two frame for object detection
ret,frame1 = cap.read()
ret,frame2 = cap.read()
frame1 = cv2.GaussianBlur(frame1, (5,5), 0)
frame2 = cv2.GaussianBlur(frame2, (5,5), 0)
while(1):
    #the open cv does open in BGR converting it to hsv 
    imghsv1=cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)
    imghsv2=cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
    '''
    lb=cv2.getTrackbarPos('LH',"Tracking")
    lg=cv2.getTrackbarPos('LS',"Tracking")
    lr=cv2.getTrackbarPos('LV',"Tracking")

    ub=cv2.getTrackbarPos('UH',"Tracking")
    ug=cv2.getTrackbarPos('US',"Tracking")
    ur=cv2.getTrackbarPos('UV',"Tracking")
    l_b=np.array([lb,lg,lr])
    u_b=np.array([ub,ug,ur])
    '''
    #these numbers are based on exprience
    l_b=np.array([72,127,0])
    u_b=np.array([109,255,255])
    #giving the range (to find the right color on the image)
    mask1=cv2.inRange(imghsv1,l_b,u_b)
    mask2=cv2.inRange(imghsv2,l_b,u_b)
    #making a mask(deleting all other colors)
    res1=cv2.bitwise_and(frame1,frame1,mask=mask1)
    res2=cv2.bitwise_and(frame2,frame2,mask=mask2)
    #less noise
    diff=cv2.absdiff(res1,res2)
    Gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blured=cv2.GaussianBlur(Gray,(5,5),0)
    ret,thresh=cv2.threshold(blured,20,255,cv2.THRESH_BINARY)
    dilated=cv2.dilate(thresh,None,iterations=5)
    contours , hierarchy=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    x1=0
    y1=0
    if(len(contours)) > 0:
        c = max(contours, key = cv2.contourArea)
            #Find the center of the circle, and its radius of the largest detected contour.
        ((x,y), radius) = cv2.minEnclosingCircle(c)

        #Calculate the centroid of the ball, as we need to draw a circle around it.
        M = cv2.moments(c)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        #Proceed only if a ball of considerable size is detected
        if radius > 10:
            #Draw circles around the object as well as its centre
            cv2.circle(frame1, (int(x), int(y)), int(radius), (0,255,255), 2)
            cv2.circle(frame1, center, 5, (255,0,0), -1)
            pts.appendleft(center)
            #Append the detected object in the frame to pts deque structure
    for i in np.arange(1, len(pts)):
        #If no points are detected, move on.
        if(pts[i-1] == None or pts[i] == None):
            continue

        #If atleast 10 frames have direction change, proceed
        if counter >= 15 and i == 1 and pts[-15] is not None:
            #Calculate the distance between the current frame and 10th frame before
            dX = pts[-15][0] - pts[i][0]
            dY = pts[-15][1] - pts[i][1]
            (dirX, dirY) = ('', '')

            #If distance is greater than 100 pixels, considerable direction change has occured.
            if np.abs(dX) > 100:
                if (np.sign(dX) == 1):
                    dirX = 'Right'
                    print("Right")
                    pyautogui.press('right')
                else :
                    dirX ='Left'
                    print("Left")
                    pyautogui.press('left')

            if np.abs(dY) > 100:
                if (np.sign(dY) == 1):
                    dirY = 'Up'
                    print("Up")
                    pyautogui.press('up')
                else:
                    dirY ='Down'
                    print("Down")
                    pyautogui.press('down')

            #Set direction variable to the detected direction
            direction = dirX if dirX != '' else dirY

        #Draw a trailing red line to depict motion of the object.
        thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
        cv2.line(frame1, pts[i - 1], pts[i], (0, 0, 255), thickness)
        #frame1=cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        #cv2.putText(frame1,"Status : {}".format("movment"),(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
        
    counter += 1

    #showing all the Images
    cv2.imshow("Image",frame1)
    cv2.imshow("Image2",res1)
    cv2.imshow("Image3",mask1)
    frame1=frame2
    _,frame2 = cap.read()
    frame2 = cv2.GaussianBlur(frame2, (5,5), 0)
    if cv2.waitKey(1)==27:
        break
cap.release()
cv2.destroyAllWindows()