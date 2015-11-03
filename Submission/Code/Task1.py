__author__ = 'rahulkrsna'

import cv2
from sys import platform as _platform


width = 100
height = 100
row_length = 10
col_length = 10
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
absError = 0


def main():

    global yComponent
    global videoFileName
    global path
    global videoFilePath
    global width
    global height

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
    height = raw_input('Start Point in Height <number>: ')
    height = int(height)
    width = raw_input('Start Point in Width <number>: ')
    width = int(width)
    extractFrames()
    outputToFile(videoFilePath.split(".")[0]+"_"+"1.tpc", 1)

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
    global width
    global height
    # videoFilePath = '/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1.mp4'

    cap = cv2.VideoCapture(videoFilePath)
    frameNumber=0

    while cap.isOpened():
        logPrinter("#0 Cap")
        ret, frame = cap.read()

        if ret == True:
            #Extract a portion of frame
            tImage = frame[height:height+row_length, width:width+col_length]
            createSignalList(tImage,frameNumber)
            frameNumber += 1
        else:
            cap.release()

    logPrinter(frameNumber)
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
    yuvImage = cv2.cvtColor(input_image, cv2.COLOR_BGR2YUV)
    y,u,v = cv2.split(yuvImage)
    index=0

    logPrinter("#2 {0}".format(len(y)))
    logPrinter("#3 {0}".format(frameNumber))
    logPrinter("#3 {0}".format(len(yComponent)))


    for row in y:
        for col in row:
            if frameNumber == 0:
                yComponent[index] = [col]
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
    global absError

    absError = 0
    if option == 1:
        # Output to File
        with open(filename, 'w') as f:
            f.write(repr(yComponent))
    elif option == 2:
        # Encode
        computeInfoOption2()
        # Output to File
        with open(filename, 'w') as f:
            f.write(repr(yComponent_option2))
    elif option == 3:
        # Encode
        computeInfoOption3()
        # Output to File
        with open(filename, 'w') as f:
            f.write(repr(yComponent_option3))
    elif option == 4:
        # Encode
        computeInfoOption4()
        # Output to File
        with open(filename, 'w') as f:
            f.write(repr(yComponent_option4))

    print("Absolute Error is {0}".format(absError))
    print("File Saved to "+filename)

def computeInfoOption2():
    global yComponent
    global yComponent_option2
    global absError
#     S[t] = S[t-1]
    row_index = 0
    for row in yComponent:
        col_index = 0
        for item in row:
            if col_index == 0:
                yComponent_option2[row_index] = [item]
            else:
                value = float(item) - float(yComponent[row_index][col_index-1])
                absError += value
                yComponent_option2[row_index].append(value)
            col_index += 1
        row_index += 1


def computeInfoOption3():
    global yComponent
    global yComponent_option3
    global absError
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
                value = (float(yComponent[row_index][col_index-1]) + float(yComponent[row_index][col_index-2]))/float(2)
                value = float(item) - value
                absError += value
                yComponent_option3[row_index].append(value)
            col_index += 1
        row_index += 1


def computeInfoOption4():
    global yComponent
    global yComponent_option4
    global absError

    row_index = 0
    for row in yComponent:
        col_index = 0
        for item in row:
            if col_index == 0:
                yComponent_option4[row_index]=[item]
            elif col_index == 1:
                yComponent_option4[row_index].append(item)
            elif col_index < 4:
                value = (0.5 * float(yComponent[row_index][col_index-1]) + 0.5 * float(yComponent[row_index][col_index-2]))
                value = float(item) - value
                absError += value;
                yComponent_option4[row_index].append(value)
            else:
                alpha = computeAlpha1(yComponent[row_index][col_index-1],yComponent[row_index][col_index-2],
                                      yComponent[row_index][col_index-3], yComponent[row_index][col_index-4])
                if alpha < 0 :
                    alpha = 0.5

                value = (alpha * float(yComponent[row_index][col_index-1]) + (1-alpha) * float(yComponent[row_index][col_index-2]))
                value = float(item) - value
                absError += value;
                yComponent_option4[row_index].append(value)
            col_index += 1
        row_index += 1

def computeAlpha1(s1,s2,s3,s4):
    if (float(s2) - float(s4)) == 0:
        return 0.5
    alpha = (float(s1)+float(s3)-float(s3)-float(s4))/(float(s2)-float(s4))
    if(alpha < 0) or (alpha > 1):
        return 0.5
    else:
        return alpha

def logPrinter(message):
    return
    print message



def writeToVideo(videofile):
    cap = cv2.VideoCapture(videofile)

    framespersecond = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    frameheight = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    framewidth = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    framecount = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    framefourcc = cap.get(cv2.cv.CV_CAP_PROP_FOURCC)
    print("FPS {0}, Width {1}, Height {2}, Count {3}, FourCC {4}".format(framespersecond,framewidth,frameheight,
                                                                         framecount,framefourcc))
    video123 = ""
    #828601953
    video123 = cv2.VideoWriter("/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/File1.mp4",framefourcc,framespersecond,
                               (framewidth,frameheight))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            video123.write(frame)
        else:
            pass


    # video123.write(frame)
    # video123.release()
if __name__ == '__main__':
    main()