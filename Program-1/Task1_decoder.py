__author__ = 'rahulkrsna'

import numpy as np
import pickle

inputlist = None
row_length = 10
col_length = 10
yComponent_option1 = [None] * (row_length * row_length)
yComponent_option2 = [None] * (row_length * row_length)
yComponent_option3 = [None] * (row_length * row_length)
yComponent_option4 = [None] * (row_length * row_length)
outputpath = None

def main():

    path = ""
    option = 0
    # path = "/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1_1.tpc"
    # option = 1
    # path = "/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1_2.tpc"
    # option = 2
    # path = "/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1_3.tpc"
    # option = 3
    # path = "/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-2/1_4.tpc"
    # option = 4

    # read input
    getinput(path)

    # Decode
    decoder(option)

def decode_tpc(option, ippath, oppath):

    global inputpath
    global outputpath

    inputpath = ippath
    outputpath = oppath

    # Get Input
    getinput(ippath)



def getinput(path):

    global inputlist
    global yComponent_option1

    logPrinter('getinput - here', 0)
    # way to read the files
    with open(path) as f:
        inputlist = eval(f.read())


def decoder(option):

    global yComponent_option1
    global  inputlist

    logPrinter('decoder - here', 1)
    if option == 1:
        yComponent_option1 = inputlist
        printList(yComponent_option1, 2)
    elif option == 2:
        computeInfoOption2()
        printList(yComponent_option2, 2)
    elif option == 3:
        computeInfoOption3()
        printList(yComponent_option3, 2)
    elif option == 4:
        computeInfoOption4()
        printList(yComponent_option4, 2)
    else:
        print('Option Not Detected')


def computeInfoOption2():

    logPrinter('computeInfoOption2 - here', 1)
    global inputlist
    global yComponent_option2

#     S[t] = S[t-1]
    row_index = 0
    for row in inputlist:
        col_index = 0
        for item in row:
            if col_index == 0:
                yComponent_option2[row_index]=[item]
            else:
                value = float(item) + float(yComponent_option2[row_index][col_index-1])
                yComponent_option2[row_index].append(int(value))
            col_index += 1
        row_index += 1


def computeInfoOption3():

    global inputlist
    global yComponent_option3

#     S[t] = (S[t-1] + S[t-2]) / 2
    row_index = 0
    for row in inputlist:
        col_index = 0
        for item in row:
            if col_index == 0:
                yComponent_option3[row_index]=[int(item)]
            elif col_index == 1:
                yComponent_option3[row_index].append(item)
            else:
                value = (float(yComponent_option3[row_index][col_index-1]) + float(yComponent_option3[row_index][col_index-2]))/float(2)
                value += float(item)
                yComponent_option3[row_index].append(int(value))
            col_index += 1
        row_index += 1


def computeInfoOption4():

    global inputlist
    global yComponent_option4

    row_index = 0
    for row in inputlist:
        col_index = 0
        for item in row:
            if col_index == 0:
                yComponent_option4[row_index]=[int(item)]
            elif col_index == 1:
                yComponent_option4[row_index].append(int(item))
            elif col_index < 4:
                value = (0.5 * float(yComponent_option4[row_index][col_index-1]) + 0.5 * float(yComponent_option4[row_index][col_index-2]))
                value += float(item)
                yComponent_option4[row_index].append(int(value))
            else:
                alpha = computeAlpha1(yComponent_option4[row_index][col_index-1], yComponent_option4[row_index][col_index-2],
                                      yComponent_option4[row_index][col_index-3], yComponent_option4[row_index][col_index-4])
                if alpha < 0:
                    alpha = 0.5

                value = (alpha * float(yComponent_option4[row_index][col_index-1]) + (1-alpha) *
                         float(yComponent_option4[row_index][col_index-2]))
                value += float(item)
                yComponent_option4[row_index].append(int(value))
            col_index += 1
        row_index += 1


def computeAlpha1(s1, s2, s3, s4):

    if (float(s2) - float(s4)) == 0:
        return 0.5

    alpha = (float(s1)+float(s3)-float(s3)-float(s4)) / (float(s2) - float(s4))

    if(alpha < 0) or (alpha > 1):
        return 0.5
    else:
        return alpha


def printList(list, times):

    index = 0
    for item in list:
        logPrinter(item)
        index += 1
        if index == times:
            break


def logPrinter(message, option=1):

    if option == 1:
        print message


if __name__ == '__main__':
    main()