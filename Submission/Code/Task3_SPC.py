__author__ = 'ysun138'
import numpy as np
import re

numberofbits = 0
inputlist = None
bins = None
binvalues = {}
outputpath = None
bins = 0
mat = None

def getBits():

    global numberofbits

    while True:
        option = raw_input("Chose an Quantization Option \n"
                           "No Quantization ------------- 1\n"
                           "Quntaization ---------------- 2\n"
                           "Exit ------------------------ 3\n"
                           "...?")
        if option == '2':
            numberofbits = raw_input("(Quantization) Enter number of bits: ")
            numberofbits = int(numberofbits)
            getinput()
            calculateBins()
            quantize()
            output(option)
        elif option == '1':
            getinput()
            output(option)
        elif option == '3':
            break
        else:
            print("Option not valid")

def getinput():

    global mat
    global inputlist
    global inputpath

    inputpath = raw_input('Enter the File Path <F>: ')
    fframe = []
    with open(inputpath) as f:
        lines =  [x.rstrip('\n') for x in f.readlines()]
    frames = []
    r = []
    for i in range(len(lines)):
        r = []
        if not "# Frame" in lines[i]:
            line = re.sub('\s+', ',', lines[i]).strip()
            word = line.split(',')
            for w in word:
                if '\n' not in w and len(w)>0:
                    pixel = int(float(w)),0,0
                    r.append(np.array(pixel))
            frames.append(np.array(r))
        else:
            if len(frames)>0:
                fframe.append(np.array(frames))
                frames = []
    fframe.append(np.array(frames))

    mat = np.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
    # print fframe.__len__()
    for frame_index in range(0, fframe.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                mat[frame_index,i,j] = fframe[frame_index][i][j][0]


def calculateBins():

    global lowervalue
    global highervalue
    global binvalues
    global bins

    bins = 0
    binvalues = {}
    if numberofbits > 8:
        range = 1
        bins = np.arange(-255, 255, range)
    else:
        range = max(1, int(510/pow(2, numberofbits)))
        bins = np.arange(-255, 255, range)

    index = 0
    value = float(-255)
    while index <= bins.size :
        value += float(range)/2.0
        binvalues[index] = float(value)
        value += float(range)/2.0
        index += 1


def quantize():

    global bins
    global outputList
    global binvalues
    global mat
    outputList = None

    outputList = mat
    frame,rows, cols = outputList.shape

    # print outputList

    for i in range(0,frame):
        for j in range(0, rows):
            bin_list = np.digitize([value for value in outputList[i,j,:]], bins)
            for k in range(0, cols):
                outputList[i,j,k] = binvalues[bin_list[k]]

    # print outputList

def output(option):

    global inputpath
    global outputList
    global numberofbits
    global mat
    if option == '1':
        outputList = mat

    frames, row, cols = outputList.shape

    if option == '1':
        outputpath = inputpath.split(".")[0] + "_{0}.spq".format(0)
        frame_index = 0
        outfile = open(outputpath,'w')
        for i in range (0, frames):
            outfile.write('# Frame: {0}\n'.format(frame_index))
            np.savetxt(outfile, outputList[frame_index], fmt='%-7.2f')
            frame_index+=1
        print("File saved as " + outputpath)

    elif option == '2':
        outputpath = inputpath.split(".")[0] + "_{0}.spq".format(numberofbits)
        outfile = open(outputpath,'w')
        frame_index = 0
        for i in range (0, frames):
            outfile.write('# Frame: {0}\n'.format(frame_index))
            np.savetxt(outfile, outputList[frame_index], fmt='%-7.2f')
            frame_index+=1
        print("File saved as " + outputpath)


def main():
    getBits()


if __name__ == '__main__':
    main()