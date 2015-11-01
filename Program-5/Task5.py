__author__ = 'kvivekan'

import arcode
import os
import cv2
import numpy
import re
import sys
sys.path.append('../Program-4/')
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

def decompress(option, encoded_file, decoded_file):
    global byteArr
    global bitPosition
    if option == "1":
        print "no compression"
        file = open(decoded_file, 'w')
        file.write(open(encoded_file,'r').read())
        file.close()
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

            temp_decoded_file_name = file_name.rsplit("_",2)
            temp_decoded_file = temp_decoded_file_name[0] + "_dc." + file_extension

            output_file = temp_decoded_file_name[0] + "." + file_extension
            predictive_coding_option = temp_decoded_file_name[0].rsplit("_",1)[1]
            decode(predictive_coding_option, temp_output_file, output_file)

            view(output_file, file_extension)

            print("\n/****************************************************************/\n")
        else:
            print("Chosen option is not valid \n")

def combine_tpv(input_file_name):
    with open(input_file_name) as f:
        list2 = eval(f.read())

    row_length = 3
    col_length = 3

    numpy.set_printoptions(threshold='nan')
    frames=numpy.array([numpy.array(xi) for xi in list2])
    print frames

    frames = numpy.transpose(frames)
    # print "transpose "
    # print frames
    count = 0
    window = []
    for i in range(len(frames)):
        l = []
        r = []
        for j in range(len(frames[i])):
            if j == 0:
                t = frames[i][j],0,0
                l.append(numpy.array((t)))
                continue
            if j%col_length == 0:
                # print "\n"
                # print frames[i][j],
                r.append(l)
                l = []
                t = frames[i][j],0,0
                l.append(numpy.array((t)).astype(numpy.uint8))
            else:
                t = frames[i][j],0,0
                l.append(numpy.array((t)).astype(numpy.uint8))
        r.append(numpy.array(l).astype(numpy.uint8))
        window.append(numpy.array(r).astype(numpy.uint8))

    # for i in range(len(window)):
    #     print "frame #: " + str(i)
    #     print window[i]

    for ff in window:
        if len(ff)>0:
            cv2.imshow('video', ff)
            if (cv2.waitKey(10) & 0xFF) == ord('q'): # Hit `q` to exit
                break
            f = '{:04}'.format(count)
            name = "frame"+f+".jpg"
            count+=1
            yframes = cv2.cvtColor(ff, cv2.COLOR_YUV2BGR)
            cv2.imwrite(name, yframes)
    print "tst"

def combine_spv(input_file_name):
    fframe = []
    count = 0
    # with open('../Program-4/2_1_1_1.spv') as f:
    with open(input_file_name) as f:
        lines =  [x.rstrip('\n') for x in f.readlines()]
    frames = []
    r = []
    for i in range(len(lines)):
        r = []
        if not "#" in lines[i]:
            line = re.sub('\s+', ',', lines[i]).strip()
            word = line.split(',')
            for w in word:
                if '\n' not in w and len(w)>0:
                    pixel = int(float(w)),0,0
                    p = numpy.array(pixel, dtype= numpy.uint8)
                    # r.append(numpy.array(pixel).astype(numpy.uint8))
                    r.append(p)
            frames.append(numpy.array(r).astype(numpy.uint8))
        else:
            if len(frames)>0:
                fframe.append(numpy.array(frames).astype(numpy.uint8))
                frames = []
    fframe.append(numpy.array(frames).astype(numpy.uint8))

    for ff in fframe:
        if len(ff)>0:
            cv2.imshow('video', ff)
            if (cv2.waitKey(10) & 0xFF) == ord('q'): # Hit `q` to exit
                break
            f = '{:04}'.format(count)
            name = "frame"+f+".jpg"
            count+=1
            yframes = cv2.cvtColor(ff, cv2.COLOR_YUV2BGR)
            cv2.imwrite(name, yframes)
    print "tst"

def decode(compression_option, input_dc_file, output_file):
    fframe = []
    count = 0
    with open(input_dc_file) as f:
        lines =  [x.rstrip('\n') for x in f.readlines()]
    frames = []
    r = []
    for i in range(len(lines)):
        r = []
        if not "#" in lines[i]:
            line = re.sub('\s+', ',', lines[i]).strip()
            word = line.split(',')
            for w in word:
                if '\n' not in w and len(w)>0:
                    pixel = int(float(w)),0,0
                    r.append(numpy.array(pixel))
            frames.append(numpy.array(r))
        else:
            if len(frames)>0:
                fframe.append(numpy.array(frames))
                frames = []
    fframe.append(numpy.array(frames))

    mat = numpy.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
    print fframe.__len__()
    for frame_index in range(0, fframe.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                if len(fframe[frame_index])>0:
                    mat[frame_index,i,j] = fframe[frame_index][i][j][0]

    original_mat =   numpy.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
    outfile = open(output_file,'w')
    frame_index = 0
    if(compression_option == 1):
        for frame_index in range(0, fframe.__len__()):
            for i in range(0, 10):
                for j in range(0,10):
                    original_mat[frame_index,i,j] = mat[frame_index,i,j]

    elif(compression_option == 2):
        for frame_index in range(0, fframe.__len__()):
            for i in range (0, 10):
                original_mat[frame_index, i, 0] = mat[frame_index, i,0]

            for i in range (0, 10):
                for j in range(1, 10):
                    original_mat[frame_index, i, j] = float(mat[frame_index, i, j]) + float(original_mat[frame_index, i,j-1])

    elif(compression_option == 3):
        for frame_index in range(0, fframe.__len__()):
            for j in range (0, 10):
                original_mat[frame_index, 0, j] = mat[frame_index, 0,j]

            for i in range (1, 10):
                    for j in range(0, 10):
                        original_mat[frame_index, i, j] = float(mat[frame_index, i, j]) + float(original_mat[frame_index, i-1,j])

    elif(compression_option == 4):
        for frame_index in range(0, fframe.__len__()):
            for j in range (0, 10):
                original_mat[frame_index, 0, j] = mat[frame_index, 0,j]

            for i in range(0, 10):
                original_mat[frame_index, i, 0] = mat[frame_index, i,0]

            for i in range (1, 10):
                for j in range(1, 10):
                    original_mat[frame_index, i, j] = float(mat[frame_index, i, j]) + float(original_mat[frame_index, i-1,j-1])

    elif(compression_option == 5):
        for frame_index in range(0, fframe.__len__()):
            for j in range (0, 10):
                original_mat[frame_index, 0, j] = mat[frame_index, 0,j]

            for i in range(0, 10):
                original_mat[frame_index, i, 0] = mat[frame_index, i,0]

            for i in range (1, 10):
                for j in range(1, 10):
                        original_mat[frame_index, i, j] = float(mat[frame_index, i, j]) + 1.0/3*(float(original_mat[frame_index, i-1,j-1])+float(original_mat[frame_index, i-1, j]+float(original_mat[frame_index, i, j-1])))

    frame_index = 0
    for frame in original_mat:
        outfile.write('# Frame: {0}\n'.format(frame_index))
        numpy.savetxt(outfile, frame, fmt='%-7.2f')
        frame_index+=1


def combine(ext, output):
    # Arguments
    dir_path = '.'
    images = []
    for f in sorted(os.listdir(dir_path)):
        if f.endswith(ext):
            images.append(f)

    # Determine the width and height from the first image
    image_path = os.path.join(dir_path, images[0])
    frame = cv2.imread(image_path)
    cv2.imshow('video',frame)
    height, width, channels = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.cv.CV_FOURCC(*'mp4v') # Be sure to use lower case
    out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))

    for image in images:

        image_path = os.path.join(dir_path, image)
        frame = cv2.imread(image_path)
        if(len(frame)>0):
            out.write(frame) # Write out frame to video
            cv2.imshow('video',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break

    # Release everything if job is finished
    out.release()
    cv2.destroyAllWindows()

    print("The output video is {}".format(output))

    for f in sorted(os.listdir(dir_path)):
        file_path = os.path.join(dir_path, f)
        if f.endswith(ext):
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e


def view(temp_decoded_file, file_extension):
    if 'spv' in file_extension:
        combine_spv(temp_decoded_file)
    elif 'tpv' in file_extension:
        combine_tpv(temp_decoded_file)
    combine('jpg','output_'+temp_decoded_file+'.mp4')

#main
main()

