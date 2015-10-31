__author__ = 'kvivekan'

import os
import lzw
import arcode
from sys import platform as _platform

def main():
    path = raw_input("Enter .tpq or .spq filename: ")
    if _platform == "linux" or _platform == "linux2":
        slash = '/'
    elif _platform == "darwin":
        slash = '/'
    elif _platform == "win32":
        slash = '\\'

    input_file = open(path, 'r')
    # print input_file.read()

    while True:
        option = raw_input("Select encoding scheme:  "
                           "\n 1: No compression"
                           "\n 2: Shannon-Fano coding"
                           "\n 3: LZW coding"
                           "\n 4: Arithmetic coding"
                           "\n 5: 5 "
                           "\n ..? ")

        if option == "5":
            print("/******************************END*********************************/")
            break
        elif option == "1" or option == "2" or option == "3" or option == "4":
            print("\n/****************************************************************/\n")
            file_extension = path.rsplit(".", 1)
            output_file_extension = ""
            if file_extension[1] == "tpq":
                output_file_extension = "tpv"
            elif file_extension[1] == "spq":
                output_file_extension = "spv"

            fileName = str(file_extension[0]) + "_" + str(option) + "." + output_file_extension

            compressToOutputFile(path, fileName,int(option))
            print("\n/****************************************************************/\n")
        else:
            print("Chosen option is not valid \n")


def shannon_fano_encoder(iA, iB): # iA to iB : index interval
    global tupleList
    size = iB - iA + 1
    if size > 1:
        # Divide the list into 2 groups.
        # Top group will get 0, bottom 1 as the new encoding bit.
        mid = int(size / 2 + iA)
        for i in range(iA, iB + 1):
            tup = tupleList[i]
            if i < mid: # top group
                tupleList[i] = (tup[0], tup[1], tup[2] + '0')
            else: # bottom group
                tupleList[i] = (tup[0], tup[1], tup[2] + '1')
        # do recursive calls for both groupszy
        shannon_fano_encoder(iA, mid - 1)
        shannon_fano_encoder(mid, iB)

def byteWriter(bitStr, outputFile):
    global bitStream
    bitStream += bitStr
    while len(bitStream) > 8: # write byte(s) if there are more then 8 bits
        byteStr = bitStream[:8]
        bitStream = bitStream[8:]
        outputFile.write(chr(int(byteStr, 2)))

def print_file_size(path):
        # read the whole input file into a byte array
        fileName = str(os.path.abspath(path))
        fileSize = os.path.getsize(fileName)
        fi = open(fileName, 'rb')
        # byteArr = map(ord, fi.read(fileSize))
        byteArr = bytearray(fi.read(fileSize))
        fi.close()
        fileSize = len(byteArr)
        # print 'File size in bytes:', fileSize
        print fileSize

def bitReader(n): # number of bits to read
    global byteArr
    global bitPosition
    bitStr = ''
    for i in range(n):
        bitPosInByte = 7 - (bitPosition % 8)
        bytePosition = int(bitPosition / 8)
        byteVal = byteArr[bytePosition]
        bitVal = int(byteVal / (2 ** bitPosInByte)) % 2
        bitStr += str(bitVal)
        bitPosition += 1 # prepare to read the next bit
    return bitStr


def compressToOutputFile(input_file, output_file_name, option):
    print ("fileName: " + output_file_name)
    print ("option: " + str(option))
    global tupleList
    global bitStream
    if option == 1:
        file = open(output_file_name, 'w')
        file.write(open(input_file,'r').read())
        file.close()
        print "Size of input file in bytes: "
        print_file_size(input_file)
        print "Size of output file ("+ output_file_name +") in bytes: "
        print_file_size(output_file_name)

    if option == 2:
        # read the whole input file into a byte array
        fileSize = os.path.getsize(str(os.path.abspath((input_file))))
        fi = open(input_file, 'rb')
        # byteArr = map(ord, fi.read(fileSize))
        byteArr = bytearray(fi.read(fileSize))
        fi.close()
        fileSize = len(byteArr)
        print "Size of input file in bytes: ", fileSize

         # calculate the total number of each byte value in the file
        freqList = [0] * 256
        for b in byteArr:
            freqList[b] += 1

        # create a list of (frequency, byteValue, encodingBitStr) tuples
        tupleList = []
        for b in range(256):
            if freqList[b] > 0:
                tupleList.append((freqList[b], b, ''))

        # sort the list according to the frequencies descending
        tupleList = sorted(tupleList, key=lambda tup: tup[0], reverse = True)

        shannon_fano_encoder(0, len(tupleList) - 1)
        # print 'The list of (frequency, byteValue, encodingBitStr) tuples:'
        # print tupleList
        # print

        # create a dictionary of byteValue : encodingBitStr pairs
        dic = dict([(tup[1], tup[2]) for tup in tupleList])
        del tupleList # unneeded anymore
        # print 'The dictionary of byteValue : encodingBitStr pairs:'
        # print dic

        # write a list of (byteValue,3-bit(len(encodingBitStr)-1),encodingBitStr)
        # tuples as the compressed file header
        bitStream = ''
        fo = open(output_file_name, 'wb')
        fo.write(chr(len(dic) - 1)) # first write the number of encoding tuples
        for (byteValue, encodingBitStr) in dic.iteritems():
            # convert the byteValue into 8-bit and send to be written into file
            bitStr = bin(byteValue)
            bitStr = bitStr[2:] # remove 0b
            bitStr = '0' * (8 - len(bitStr)) + bitStr # add 0's if needed for 8 bits
            byteWriter(bitStr, fo)
            # convert len(encodingBitStr) to 3-bit and send to be written into file
            bitStr = bin(len(encodingBitStr) - 1) # 0b0 to 0b111
            bitStr = bitStr[2:] # remove 0b
            bitStr = '0' * (3 - len(bitStr)) + bitStr # add 0's if needed for 3 bits
            byteWriter(bitStr, fo)
            # send encodingBitStr to be written into file
            byteWriter(encodingBitStr, fo)

        # write 32-bit (input file size)-1 value
        bitStr = bin(fileSize - 1)
        bitStr = bitStr[2:] # remove 0b
        bitStr = '0' * (32 - len(bitStr)) + bitStr # add 0's if needed for 32 bits
        byteWriter(bitStr, fo)

        # write the encoded data
        for b in byteArr:
            byteWriter(dic[b], fo)

        byteWriter('0' * 8, fo) # to write the last remaining bits (if any)
        fo.close()

        print "Size of compressed putput file ("+ output_file_name +") in bytes: "
        print_file_size(output_file_name)

    if option == 3:

        print "Size of input file in bytes: "
        print_file_size(input_file)
        mybytes = lzw.readbytes(input_file)
        lessbytes = lzw.compress(mybytes)
        lzw.writebytes(output_file_name, lessbytes)
        print "Size of compressed putput file ("+ output_file_name +") in bytes: "
        print_file_size(output_file_name)

    if option == 4:

        print "Size of input file in bytes: "
        print_file_size(input_file)
        ar = arcode.ArithmeticCode(False)
        ar.encode_file(input_file, output_file_name)
        print "Size of compressed putput file ("+ output_file_name +") in bytes: "
        print_file_size(output_file_name)

#main
main()
