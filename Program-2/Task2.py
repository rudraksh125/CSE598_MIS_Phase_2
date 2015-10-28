__author__ = 'ysun138'

import cv2
import numpy as np
from sys import platform as _platform

def Coding(cap, top_left_x, top_left_y, choice):
    error = 0
    if(choice == 1):
        frame_index = 0
        outfile = open("D:\YuhanSun\\598\\Phase2\{0}_{1}.spc".format(filename.split(".")[0], choice),'w')
        while(cap.isOpened):
            ret, frame = cap.read()
            if(ret):
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yuv = yuv[frameStartX:frameStartX+10,frameStartY:frameStartY+10,0]
                rows, cols = yuv.shape
                outfile.write('# Frame: {0}\n'.format(frame_index))
                np.savetxt(outfile, yuv, fmt='%-7.2f')
                frame_index+=1
            else:
                break
    elif(choice == 2):
        frame_index = 0
        outfile = open("D:\YuhanSun\\598\\Phase2\{0}_{1}.spc".format(filename.split(".")[0], choice),'w')
        while(cap.isOpened):
            ret, frame = cap.read()
            if(ret):
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yuv = yuv[frameStartX:frameStartX+10,frameStartY:frameStartY+10,0]
                rows, cols = yuv.shape
                compress_yuv = np.ndarray((rows,cols), dtype = float, order = 'F')

                for i in range (0, rows):
                    compress_yuv[i, 0] = yuv[i,0]

                for i in range (0, rows):
                    for j in range(1, cols):
                        compress_yuv[i, j] = float(yuv[i, j]) - float(yuv[i,j-1])
                        error+=abs(compress_yuv[i,j])

                outfile.write('# Frame: {0}\n'.format(frame_index))
                np.savetxt(outfile, compress_yuv, fmt='%-7.2f')
                frame_index+=1
            else:
                break
    elif(choice == 3):
        frame_index = 0
        outfile = open("D:\YuhanSun\\598\\Phase2\{0}_{1}.spc".format(filename.split(".")[0], choice),'w')
        while(cap.isOpened):
            ret, frame = cap.read()
            if(ret):
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yuv = yuv[frameStartX:frameStartX+10,frameStartY:frameStartY+10,0]
                rows, cols = yuv.shape
                compress_yuv = np.ndarray((rows,cols), dtype = float, order = 'F')

                for j in range (0, cols):
                    compress_yuv[0, j] = yuv[0,j]

                for i in range (1, rows):
                    for j in range(0, cols):
                        compress_yuv[i, j] = float(yuv[i, j]) - float(yuv[i-1,j])
                        error+=abs(compress_yuv[i,j])

                outfile.write('# Frame: {0}\n'.format(frame_index))
                np.savetxt(outfile, compress_yuv, fmt='%-7.2f')
                frame_index+=1
            else:
                break
    elif(choice ==4 ):
        frame_index = 0
        outfile = open("D:\YuhanSun\\598\\Phase2\{0}_{1}.spc".format(filename.split(".")[0], choice),'w')
        while(cap.isOpened):
            ret, frame = cap.read()
            if(ret):
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yuv = yuv[frameStartX:frameStartX+10,frameStartY:frameStartY+10,0]
                rows, cols = yuv.shape
                compress_yuv = np.ndarray((rows,cols), dtype = float, order = 'F')

                for j in range (0, cols):
                    compress_yuv[0, j] = yuv[0,j]

                for i in range(0, rows):
                    compress_yuv[i, 0] = yuv[i,0]

                for i in range (1, rows):
                    for j in range(1, cols):
                        compress_yuv[i, j] = float(yuv[i, j]) - float(yuv[i-1,j-1])
                        error+=abs(compress_yuv[i,j])

                outfile.write('# Frame: {0}\n'.format(frame_index))
                np.savetxt(outfile, compress_yuv, fmt='%-7.2f')
                frame_index+=1
            else:
                break
    elif(choice ==5 ):
        frame_index = 0
        outfile = open("D:\YuhanSun\\598\\Phase2\{0}_{1}.spc".format(filename.split(".")[0], choice),'w')
        while(cap.isOpened):
            ret, frame = cap.read()
            if(ret):
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yuv = yuv[frameStartX:frameStartX+10,frameStartY:frameStartY+10,0]
                rows, cols = yuv.shape
                compress_yuv = np.ndarray((rows,cols), dtype = float, order = 'F')

                for j in range (0, cols):
                    compress_yuv[0, j] = yuv[0,j]

                for i in range(0, rows):
                    compress_yuv[i, 0] = yuv[i,0]

                for i in range (1, rows):
                    for j in range(1, cols):
                        compress_yuv[i, j] = float(yuv[i, j]) - 1.0/3*(float(yuv[i-1,j-1])+float(yuv[i-1, j]+float(yuv[i, j-1])))
                        error+=abs(compress_yuv[i,j])

                outfile.write('# Frame: {0}\n'.format(frame_index))
                np.savetxt(outfile, compress_yuv, fmt='%-7.2f')
                frame_index+=1
            else:
                break
    outfile.write("#Prediction error is "+str(error))
    outfile.close()

    print "\n### File saved as {0}_{1}.spc ###".format(filename.split(".")[0], choice)

    print "\nPrediction error is "+str(error)
def main():

    print("### Spatial Predictive Coding [SPC] ###\n")
    global filename
    global frameStartX
    global frameStartY
    while(1):
        filename = raw_input("Enter the make of the video file: ")

        frameStartX = int(raw_input("\nEnter the top-left X coordinate: "))
        frameStartY = int(raw_input("Enter the top-left Y coordinate: "))

        print("\n### Reading the file ###\n")

        choice = int(raw_input("Select any one of the following:\nPress 1 for No PC\nPress 2 for Predictor A\nPress 3 for Predictor B\nPress 4 for Predictor C\nPress 5 for Alpha-based Predictor\nChoice : "))

        print("\n### You select option {0} ###".format(choice))

        print("\n### Calculating the encoding ###")

        videoFile = 'D:\YuhanSun\\598\\{0}'.format(filename)
        cap = cv2.VideoCapture(videoFile)
        Coding(cap, frameStartX, frameStartY, 5)

        user_input = raw_input("\nDo you want to continue Y/N: ")
        if(user_input.__eq__('N')):
            break

if __name__ == '__main__':
    main()