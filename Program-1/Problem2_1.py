__author__ = 'rahulkrsna'

import cv2
import numpy as np
import pickle
from sys import platform as _platform


frameStartX = 10
frameStartY = 10
row_length = 3
col_length = 3
yComponent = [None] * (row_length * row_length)
yComponent_option2 = [None] * (row_length * row_length)
yComponent_option3 = [None] * (row_length * row_length)
yComponent_option4 = [None] * (row_length * row_length)
option2_absoluteDiff = 0
option3_absoluteDiff = 0
option4_absoluteDiff = 0
videoFileName = ""
path = ""
videoFilePath = ""

def main():

    global yComponent
    global videoFileName
    global path
    global videoFilePath

    #capture frame numbers as input.
    path = raw_input("Enter the Path of Folder containing video Files: ")
    if _platform == "linux" or _platform == "linux2":
        slash = '/'
    elif _platform == "darwin":
        slash = '/'
    elif _platform == "win32":
        slash = '\\'

    path.rstrip(slash)
    path = path + slash

    videoFileName = raw_input('Enter the video file name <v>: ')
    videoFilePath = path+videoFileName
    extractFrames()

    while True:
        option = raw_input("Chose a Predictive Coding Option "
                           "\n No Predictive Coding  ---------------------------------------------- 1"
                           "\n Predictive Coding S[t] = S[t-1] ------------------------------------ 2"
                           "\n Predictive Coding S[t] = (S[t-1] + S[t-2])/2 ----------------------- 3"
                           "\n Predictive Coding S[t] = alpha1 * S[t-1]  + alpha2 * S[t-2] -------- 4"
                           "\n Exit  -------------------------------------------------------------- 5 "
                           "\n ..? ")

        if option == "5":
            print("/******************************END*********************************/")
            break
        elif option == "1" or option == "2" or option == "3" or option == "4":
            print("\n/****************************************************************/\n")
            fileName = videoFilePath.split(".")[0]+"_"+option+".tpc"
            outputToFile(fileName,int(option))
            print("\n/****************************************************************/\n")
        else:
            print("Chosen option is not valid \n")


# Extracts Frames and Saves the partial frame information
def extractFrames():
    global videoFilePath
    # videoFilePath = '/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1.mp4'

    cap = cv2.VideoCapture(videoFilePath)

    frameNumber=0
    while cap.isOpened():
        logPrinter("#0 Cap")
        ret, frame = cap.read()
        if ret == True:
            #Extract a portion of frame
            tImage = frame[frameStartX:frameStartX+row_length, frameStartY:frameStartY+col_length]
            createSignalList(tImage,frameNumber)
            frameNumber += 1
            if(frameNumber == 20):
                cap.release()
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
    logPrinter(yComponent)

# Creates a Signal list for every frame
def createSignalList(input_image, frameNumber):
    global yComponent

    logPrinter('#1')
    #Convert to YUV image
    yuvImage = cv2.cvtColor(input_image,cv2.COLOR_BGR2YUV)
    y,u,v = cv2.split(yuvImage)
    index=0
    logPrinter("#2 {0}".format(len(y)))
    logPrinter("#3 {0}".format(frameNumber))
    logPrinter("#3 {0}".format(len(yComponent)))

    for row in y:
        for col in row:
            if frameNumber == 0:
                yComponent[index]=[col]
            else:
                yComponent[index].append(col)
            index+=1

    logPrinter(len(yComponent))
    logPrinter('#2 - end')

# This method computes the Predictive Coding Error values basing on the predictive function
# Then outputs the error values to files.
def outputToFile(filename, option):
    global yComponent
    global yComponent_option2
    global yComponent_option3
    global yComponent_option4

    if option == 1:
        # Output to File
        with open(filename, 'w') as f:
            f.write(repr(yComponent))
        # Print Info
        for row in yComponent:
            print row
    if option == 2:
        # Encode
        computeInfoOption2()
        # Output to File
        with open(filename, 'w') as f:
            f.write(repr(yComponent_option2))
        # Print Info
        for row in yComponent_option2:
            print row

    if option == 3:
        # Encode
        computeInfoOption3()
        # Output to File
        with open(filename, 'w') as f:
            f.write(repr(yComponent_option3))
        #Print Info
        for row in yComponent_option3:
            print row

    if option == 4:
        # Encode
        computeInfoOption4()
        # Output to File
        with open(filename, 'w') as f:
            f.write(repr(yComponent_option4))
        #Print Info
        for row in yComponent_option4:
            print row


def computeInfoOption2():
    global yComponent
    global yComponent_option2
    global option2_absoluteDiff
#     S[t] = S[t-1]
    row_index = 0
    for row in yComponent:
        col_index = 0
        for item in row:
            if col_index == 0:
                yComponent_option2[row_index]=[item]
            else:
                value = int(item) - int(yComponent[row_index][col_index-1])
                option2_absoluteDiff += value
                yComponent_option2[row_index].append(value)
            col_index += 1
        row_index += 1


def computeInfoOption3():
    global yComponent
    global yComponent_option3
#     S[t] = (S[t-1] + S[t-2]) / 2
    row_index = 0
    for row in yComponent:
        col_index = 0
        for item in row:
            if col_index == 0:
                yComponent_option3[row_index]=[item]
            elif col_index == 1:
                yComponent_option3[row_index].append(item)
            else:
                value = (int(yComponent[row_index][col_index-1]) + int(yComponent[row_index][col_index-2]))/2
                value = int(item) - value
                yComponent_option3[row_index].append(value)
            col_index += 1
        row_index += 1


def computeInfoOption4():
    global yComponent
    global yComponent_option4

    row_index = 0
    for row in yComponent:
        col_index = 0
        for item in row:
            if col_index == 0:
                yComponent_option4[row_index]=[item]
            elif col_index == 1:
                yComponent_option4[row_index].append(item)
            elif col_index < 4:
                value = (0.5 * int(yComponent[row_index][col_index-1]) + 0.5 * int(yComponent[row_index][col_index-2]))
                value = int(item) - value
                yComponent_option4[row_index].append(value)
            else:
                alpha = computeAlpha1(yComponent[row_index][col_index-1],yComponent[row_index][col_index-2], yComponent[row_index][col_index-3], yComponent[row_index][col_index-4])
                if alpha < 0 :
                    alpha = 0.5

                value = (alpha * int(yComponent[row_index][col_index-1]) + (1-alpha) * int(yComponent[row_index][col_index-2]))
                value = int(item) - value
                yComponent_option4[row_index].append(value)
            col_index += 1
        row_index += 1

def computeAlpha1(s1,s2,s3,s4):
    if int(s2) - int(s4) == 0 :
        return 0.5
    return (int(s1)+int(s3)-int(s3)-int(s4))/(int(s2)-int(s4))

def logPrinter(message):
    return
    print message

# way to read the files
# with open('tem2.txt') as f:
#     list2 = eval(f.read())

if __name__ == '__main__':
    main()