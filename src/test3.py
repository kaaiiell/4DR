import numpy as np
import cv2
import time
import os, os.path
import SingleCheckerboard as sc
from random import randrange

def createLine(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Creating Line for " + param[0])
        print(param[1])
        if param[0] == "Frame1":
            imageIndex = 1
            otherIndex = 2
        else:
            imageIndex = 2
            otherIndex = 1

        color = (randrange(256), randrange(256) , randrange(256))

        point = np.array([x,y])
        line = [0,0,0]
        line = cv2.computeCorrespondEpilines(point.reshape(-1,1,2), imageIndex, param[1])
        line = line[0][0]
        size = param[2].shape[1]
        x0, y0 = map(int, [0, -line[2]/line[1]])
        x1, y1 = map(int, [size, -(line[2]+(line[0]*float(size)))/line[1]])
        cv2.line(param[2], (x0, y0),(x1, y1),color, 2)

        point = np.array([x1,y1])
        line = [0,0,0]
        line = cv2.computeCorrespondEpilines(point.reshape(-1,1,2), otherIndex, param[1])
        line = line[0][0]
        x0, y0 = map(int, [0, -line[2]/line[1]])
        x1, y1 = map(int, [size, -(line[2]+(line[0]*float(size)))/line[1]])
        cv2.line(param[3], (x0, y0),(x1, y1),color, 2)
        


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

ret1, frame1 = cap1.read()
ret2, frame2 = cap2.read()

directory = "images"
list = os.listdir(directory)
number_files = len(list)
print(number_files)


start = 0
frameNum = 0



while(True):

    while(True):
        if frameNum == 0:
            start = time.time()
        
        
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        saveFrame1 = frame1.copy()
        saveFrame2 = frame2.copy()
        
        # Our operations on the frame come here
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)            
        gray1 = np.float32(gray1)
        gray2 = np.float32(gray2)
        gray1 = cv2.cornerHarris(gray1,3,3,0.04)
        gray2 = cv2.cornerHarris(gray2,3,3,0.04)
        gray1 = cv2.dilate(gray1,None)
        gray2 = cv2.dilate(gray2,None)
        frame1[gray1>0.01*gray1.max()]=[0,0,255]
        frame2[gray2>0.01*gray2.max()]=[0,0,255]

        cv2.imshow('Frame1',frame1)
        cv2.imshow('Frame2',frame2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Capturing images")
            number_files += 1
            title = "images/" + str(number_files) + ".jpg"
            cv2.imwrite(title, saveFrame1)
            number_files += 1
            title = "images/" + str(number_files) + ".jpg"
            cv2.imwrite(title, saveFrame2)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cap1.release()
            cap2.release()
            break

        frameNum += 1
        if frameNum == 45:
            end = time.time()
            fps = frameNum/(end-start)
            frameNum = 0
            print(fps)
    
    print("Take Another Photo? Y = Yes, N = No")
    choice = input()
    if(choice == 'Y'):
        cap1 = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)
        continue
    else:
        break

for i in range(1, number_files, 2):
    index = i
    imgname1 = str(index)+ ".jpg"
    index += 1
    imgname2 = str(index) + ".jpg"

    if(os.path.isfile("images/" + imgname1) == False):
        continue
    
    img1 = cv2.imread("images/" + imgname1)
    img2 = cv2.imread("images/" + imgname2)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret1, temp = cv2.findChessboardCorners(gray1, (8,6), None)
    ret2, temp = cv2.findChessboardCorners(gray2, (8,6), None)

    if (ret1 and ret2) == True:
        continue
    else:
        try: 
            os.remove("images/" + imgname1)
            os.remove("images/" + imgname2)
        except: pass

objp = np.zeros((6*8,3),np.float32)
objp[:,:2] = .25*(np.mgrid[0:8,0:6].T.reshape(-1,2))

objpoints1 = []
imgpoints1 = []
objpoints2 = []
imgpoints2 = []
objpoints = []

for i in range(1, number_files, 2):
    index = i
    imgname1 = str(index)+ ".jpg"
    index += 1
    imgname2 = str(index) + ".jpg"
    print(index)

    if(os.path.isfile("images/" + imgname1) == False):
        continue
    
    frame1 = cv2.imread("images/" + imgname1)
    frame2 = cv2.imread("images/" + imgname2)

    
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    ret, corners = cv2.findChessboardCorners(gray1, (8,6), None)
    objpoints1.append(objp)
    corners2 = cv2.cornerSubPix(gray1, corners, (11,11), (-1,-1), criteria)
    imgpoints1.append(corners2)

    ret, corners = cv2.findChessboardCorners(gray2, (8,6), None)
    objpoints2.append(objp)
    corners2 = cv2.cornerSubPix(gray2, corners, (11,11), (-1,-1), criteria)
    imgpoints2.append(corners2)


    objpoints.append(objp)
    
print(gray1.shape[::-1],gray2.shape[::-1])
    
mtx1, dist1, roi1, newmtx1 = sc.getInternalCharacteristics(0)
mtx2, dist2, roi2, newmtx2 = sc.getInternalCharacteristics(1)

print(mtx1)
print(dist1)
print(mtx2)
print(dist2)



ret, a, b, c, d, Rmtx, Tmtx, Emtx, Fmtx = cv2.stereoCalibrate(objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2, gray2.shape[::-1], 256, criteria)
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
while(True):
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    cv2.imshow('Frame1',frame1)
    cv2.imshow('Frame2',frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()
        break

h = gray1.shape[0]
w = gray1.shape[1]
print(mtx1.shape)
print(newmtx1.shape)

frame1 = cv2.undistort(frame1,mtx1,dist1, None, newmtx1)
frame2 = cv2.undistort(frame2,mtx2,dist2, None, newmtx2)

x,y,w,h = roi1
frame1 = frame1[y:y+h,x:x+w]
print(roi1)
x,y,w,h = roi2
print(roi2)
frame2 = frame2[y:y+h,x:x+w]

cv2.namedWindow('Frame1')
cv2.namedWindow('Frame2')
cv2.imshow('Frame1',frame1)
cv2.imshow('Frame2',frame2)
cv2.waitKey(1)
cv2.setMouseCallback('Frame1',createLine, ["Frame1", Fmtx, frame2, frame1])
cv2.setMouseCallback('Frame2',createLine, ["Frame2", Fmtx, frame1, frame2])

while(True):
    cv2.imshow('Frame1',frame1)
    cv2.imshow('Frame2',frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


