__author__ = 'rahulkrsna'

import cv2
import numpy as np
from sys import platform as _platform

yComponent = [None] * 100
frameStartX = 10
frameStartY = 10

def main():

    global yComponent
    #capture frame numbers as input.
    # path = raw_input("Enter the Path of Folder containing video Files:\n")
    # if _platform == "linux" or _platform == "linux2":
    #     slash = '/'
    # elif _platform == "darwin":
    #     slash = '/'
    # elif _platform == "win32":
    #     slash = '\\'
    #
    # path.rstrip(slash)
    # path = path + slash
    #
    # file = raw_input('Enter the video file name <v>: ')
    # videoFile = path+videoFile

    videoFile = '/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1.mp4'


    cap = cv2.VideoCapture(videoFile)

    # Frame Count
    # framecount = 0
    # if cap.isOpened():
    #     framecount = int(cap.get(7)) # get the framecount
    #
    #
    # print "Frames: {0} ".format(framecount)

    frameNumber=0
    while cap.isOpened():
        logPrinter("#0 Cap")
        ret, frame = cap.read()
        if ret == True:
            #Extract a portion of frame
            tImage = frame[frameStartX:frameStartX+10, frameStartY:frameStartY+10]
            createSignalList(tImage,frameNumber)
            frameNumber+=1
            # if(frameNumber == 2):
            #     cap.release()
        else:
            cap.release()
    print frameNumber
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    logPrinter("#0 Size of: {0}".format(len(yComponent)))
    cap.release()
    logPrinter("#0 yComponent")
    # print(yComponent)
    logPrinter("#############")
    print(len(yComponent[0]))



def createSignalList(input_image, frameNumber):
    global yComponent
    logPrinter('#1')
    #Convert to YUV image
    yuvImage = cv2.cvtColor(input_image,cv2.COLOR_BGR2YUV)
    y,u,v = cv2.split(yuvImage)
    index=0
    logPrinter("#2 {0}".format(len(y)))
    for row in y:
        for col in row:
            if(frameNumber == 0):
                yComponent[index]=[col]
            else:
                yComponent[index].append(col)
            index+=1

    logPrinter(len(yComponent))
    logPrinter('#2 - end')
    # yComponent.append(y)
    # print(y)
    # print(len(yComponent))

def logPrinter(message):
    return
    print message

if __name__ == '__main__':
    main()