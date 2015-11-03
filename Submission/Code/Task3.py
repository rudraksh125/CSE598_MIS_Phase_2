__author__ = 'rahulkrsna'
import numpy as np


numberofbits = 0
lowervalue = -255
highervalue = 255
inputlist = None
bins = None
binvalues = {}
outputpath = None
inputpath = None
bins = 0

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
    outputList = None

    outputList = np.array(inputlist)
    rows, cols = outputList.shape

    for i in range(0,rows):
        bin_list = np.digitize([value for value in outputList[i]], bins)
        for j in range(0, cols):
            outputList[i][j] = binvalues[bin_list[j]]

def output(option):

    global inputpath

    if option == '1':
        outputpath = inputpath.split(".")[0] + "_{0}.tpq".format(0)
        with open(outputpath, 'w') as f:
            f.write(repr(inputlist))
        print("File saved as " + outputpath)
    elif option == '2':
        outputpath = inputpath.split(".")[0] + "_{0}.tpq".format(numberofbits)
        with open(outputpath, 'w') as f:
            f.write(repr(outputList.tolist()))
        print("File saved as " + outputpath)


def getinput():

    global inputlist
    global inputpath

    logPrinter('getinput - here', 1)
    inputpath = raw_input('Enter the File Path <F>: ')
    # way to read the files
    with open(inputpath) as f:
        inputlist = eval(f.read())


def logPrinter(message, option=1):

    if option == 1:
        print message


def main():

    getBits()
    calculateBins()


if __name__ == '__main__':
    main()

'''
/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1_1.tpc
/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1_2.tpc
/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1_3.tpc
/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1_4.tpc
'''