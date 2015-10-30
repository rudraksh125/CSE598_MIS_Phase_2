import arcode
import os
import lzw
from sys import platform as _platform

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

def decode(option, decompressed_file):
    pass

def decompress(option, encoded_file, decoded_file):
    global byteArr
    global bitPosition
    if option == "1":
        print "no compression"
    if option == "2":
        # read the whole input file into a byte array
        fileSize = os.path.getsize(str(os.path.abspath((encoded_file))))
        fi = open(encoded_file, 'rb')
        # byteArr = map(ord, fi.read(fileSize))
        byteArr = bytearray(fi.read(fileSize))
        fi.close()
        fileSize = len(byteArr)
        print 'File size in bytes:', fileSize

        bitPosition = 0
        n = int(bitReader(8), 2) + 1 # first read the number of encoding tuples
        # print 'Number of encoding tuples:', n
        dic = dict()
        for i in range(n):
            # read the byteValue
            byteValue = int(bitReader(8), 2)
            # read 3-bit(len(encodingBitStr)-1) value
            m = int(bitReader(3), 2) + 1
            # read encodingBitStr
            encodingBitStr = bitReader(m)
            dic[encodingBitStr] = byteValue # add to the dictionary
        # print 'The dictionary of encodingBitStr : byteValue pairs:'
        # print dic
        # print

        # read 32-bit file size (number of encoded bytes) value
        numBytes = long(bitReader(32), 2) + 1
        print 'Number of bytes to decode:', numBytes

        # read the encoded data, decode it, write into the output file
        fo = open(decoded_file, 'wb')
        for b in range(numBytes):
            # read bits until a decoding match is found
            encodingBitStr = ''
            while True:
                encodingBitStr += bitReader(1)
                if encodingBitStr in dic:
                    byteValue = dic[encodingBitStr]
                    fo.write(chr(byteValue))
                    break
        fo.close()

    if option == "3":
        newbytes = b"".join(lzw.decompress(lzw.readbytes(encoded_file)))
        decoded = open(decoded_file, 'w')
        decoded.write(newbytes)
        print "LZW decoding num of bytes: " + str(newbytes.__sizeof__())

    if option == "4":
        ar = arcode.ArithmeticCode(False)
        ar.decode_file(encoded_file, decoded_file)

def main():
    global byteArr
    global bitPosition
    path = raw_input("Enter .tpv or .spv filename: ")
    if _platform == "linux" or _platform == "linux2":
        slash = '/'
    elif _platform == "darwin":
        slash = '/'
    elif _platform == "win32":
        slash = '\\'

    input_file = open(path, 'r')
    print input_file.read()

    while True:
        option = raw_input("Select option:  "
                           "\n 1: View file"
                           "\n 2: Enter another filename: "
                           "\n 3: Exit"
                           "\n ..? ")

        if option == "3":
            print("/******************************END*********************************/")
            break
        elif option == "2":
            path = raw_input("Enter .tpv or .spv filename: ")
        elif option == "1":
            print("\n/****************************************************************/\n")
            file_c = path.rsplit("_", 1)
            compression_option = file_c[1].split(".")[0]
            if path.count(slash) > 0:
                file_name = path.rsplit(slash,1)[1].rsplit(".",1)[0]
                file_extension = path.rsplit(slash,1)[1].rsplit(".",1)[1]
                temp_output_file = path.rsplit(slash,1)[1]+ slash + file_name + "_dc." + file_extension
            else:
                file_name = path.rsplit(".",1)[0]
                file_extension = path.rsplit(".",1)[1]
                temp_output_file = file_name + "_dc." + file_extension

            decompress(compression_option,path, temp_output_file)

            decode ("", temp_output_file)

            print("\n/****************************************************************/\n")
        else:
            print("Chosen option is not valid \n")

#main
main()

