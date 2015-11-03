__author__ = 'kvivekan'

import arcode
import os
import cv2
import numpy
import re
# import sys
# sys.path.append('../Program-1/')
import lzw
import scipy.stats
from sklearn.metrics import mean_squared_error
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
    # print input_file.read()

    while True:
        option = raw_input("Select option:  "
                           "\n 1: View file"
                           "\n 2: Exit"
                           "\n ..? ")

        if option == "2":
            print("/******************************END*********************************/")
            break
        elif option == "1":
            print("\n/****************************************************************/\n")
            file_c = path.rsplit("_", 1)
            compression_option = file_c[1].split(".")[0]
            if path.count(slash) > 0:
                file_name = path.rsplit(slash,1)[1].rsplit(".",1)[0]
                file_extension = path.rsplit(slash,1)[1].rsplit(".",1)[1]
                temp_output_file = path.rsplit(slash,1)[0]+ slash + file_name + "_dc." + file_extension
            else:
                file_name = path.rsplit(".",1)[0]
                file_extension = path.rsplit(".",1)[1]
                temp_output_file = str(file_name) + "_dc." + str(file_extension)

            decompress(compression_option,path, temp_output_file)

            temp_decoded_file_name = file_name.rsplit("_",2)
            temp_decoded_file = temp_decoded_file_name[0] + "_dc." + file_extension

            output_file = temp_decoded_file_name[0] + "." + file_extension
            predictive_coding_option = temp_decoded_file_name[0].rsplit("_",1)[1]

            if "spv" in file_extension:
                decode_spc(int(predictive_coding_option), temp_output_file, output_file)
            else:
                decode_tpc(int(predictive_coding_option),temp_output_file, output_file)

            view(output_file, file_extension)

            print "calculating distortion: "
            if "spv" in file_extension:
                original_file = temp_output_file.rsplit("_",3)[0] + "_original.spc"
                distortion_spc(int(predictive_coding_option), original_file ,temp_output_file)
            else:
                original_file = temp_output_file.rsplit("_",4)[0] + "_1.tpc"
                distortion_tpc(original_file ,output_file)


            print("\n/****************************************************************/\n")
        else:
            print("Chosen option is not valid \n")

def combine_tpv(input_file_name):

    window = construct_tp_frames(input_file_name)
    count = 0
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
    print "saved images"

def combine_spv(input_file_name):

    fframe = construct_sp_frames(input_file_name)
    count = 0

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
    print "saved images"

def decode_spc(compression_option, input_dc_file, output_file):
    fframe = construct_sp_frames(input_dc_file)
    count = 0

    mat = numpy.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
    # print fframe.__len__()
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

def distortion_tpc(original_filename, input_dc_file):

    originalFrames = construct_tp_frames(original_filename)
    decodedFrames = construct_tp_frames(input_dc_file)
#     TODO

    exact_original_mat = numpy.ndarray((originalFrames.__len__(),10,10), dtype = float, order = 'F')


    for frame_index in range(0, originalFrames.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                exact_original_mat[frame_index,i,j] = originalFrames[frame_index][i][j][0]


    mat = numpy.ndarray((decodedFrames.__len__(),10,10), dtype = float, order = 'F')


    for frame_index in range(0, decodedFrames.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                if len(decodedFrames[frame_index])>0:
                    mat[frame_index,i,j] = decodedFrames[frame_index][i][j][0]

    p_signal = 0.0
    p_noise = 0.0
    for frame_index in range(0, originalFrames.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                p_signal+=exact_original_mat[frame_index,i,j]*exact_original_mat[frame_index,i,j]
                p_noise+=(exact_original_mat[frame_index,i,j] - mat[frame_index, i, j])*(exact_original_mat[frame_index,i,j] - mat[frame_index, i, j])
    if(abs(p_noise)<0.00000001):
        print "there is no error"
    else:
        print "Total error squared / total noise squared error:"
        print (p_signal/p_noise)

    print "SNR: (mean / standard deviation)"
    snr = scipy.stats.signaltonoise(mat,axis = None)
    print snr


def construct_tp_frames(file_name):
    with open(file_name) as f:
        list2 = eval(f.read())

    row_length = 10
    col_length = 10

    numpy.set_printoptions(threshold='nan')
    frames=numpy.array([numpy.array(xi) for xi in list2])
    # print frames

    frames = numpy.transpose(frames)
    window = []
    for i in range(len(frames)):
        l = []
        r = []
        for j in range(len(frames[i])):
            if j == 0:
                t = frames[i][j],0,0
                l.append(numpy.array((t)).astype(numpy.uint8))
                continue
            if j%col_length == 0:
                r.append(l)
                l = []
                t = frames[i][j],0,0
                p = numpy.array(t, dtype= numpy.uint8)
                l.append(p)
            else:
                t = frames[i][j],0,0
                p = numpy.array(t, dtype= numpy.uint8)
                l.append(p)
        k = numpy.array(l, dtype= numpy.uint8)
        r.append(k)
        # m = numpy.array(r).astype(numpy.uint8)
        m = numpy.array(r, dtype= numpy.uint8)
        window.append(m)
    return window

def construct_sp_frames(file_name):
    fframe = []
    with open(file_name) as f:
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
                    r.append(p)
            frames.append(numpy.array(r).astype(numpy.uint8))
        else:
            if len(frames)>0:
                fframe.append(numpy.array(frames).astype(numpy.uint8))
                frames = []
    fframe.append(numpy.array(frames).astype(numpy.uint8))
    return fframe

def distortion_spc(compression_option, original_filename, input_dc_file):

    fframe = construct_sp_frames(original_filename)

    exact_original_mat = numpy.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
    # print fframe.__len__()
    for frame_index in range(0, fframe.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                exact_original_mat[frame_index,i,j] = fframe[frame_index][i][j][0]

    fframe = construct_sp_frames(input_dc_file)

    mat = numpy.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
    # print fframe.__len__()
    for frame_index in range(0, fframe.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                if len(fframe[frame_index])>0:
                    mat[frame_index,i,j] = fframe[frame_index][i][j][0]

    original_mat = numpy.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')

    # compression_option = int(input_dc_file.split("_")[1])
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

    p_signal = 0.0
    p_noise = 0.0
    for frame_index in range(0, fframe.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                p_signal+=exact_original_mat[frame_index,i,j]*exact_original_mat[frame_index,i,j]
                p_noise+=(exact_original_mat[frame_index,i,j] - original_mat[frame_index, i, j])*(exact_original_mat[frame_index,i,j] - original_mat[frame_index, i, j])
    if(abs(p_noise)<0.00000001):
        print "there is no error"
    else:
        print "Total error squared / total noise squared error:"
        print (p_signal/p_noise)

    print "SNR: (mean / standard deviation)"
    snr = scipy.stats.signaltonoise(original_mat,axis = None)
    print snr

    # print "mean squared error:"
    # mse = ((exact_original_mat - original_mat) ** 2).mean(axis=None)
    # print mse
    #
    # print "sklearn mean squared error:"
    # mse = mean_squared_error(exact_original_mat, original_mat)
    # print mse



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

inputlist = None
row_length = 10
col_length = 10
yComponent_option1 = [None] * (row_length * row_length)
yComponent_option2 = [None] * (row_length * row_length)
yComponent_option3 = [None] * (row_length * row_length)
yComponent_option4 = [None] * (row_length * row_length)
outputpath = None

def decode_tpc(option, ippath, oppath):

    global inputpath
    global outputpath

    inputpath = ippath
    outputpath = oppath

    # Get Input
    getinput(ippath)

    # Decode
    decoder(option)

    #output
    output(option, oppath)

def getinput(path):

    global inputlist
    global yComponent_option1

    # way to read the files
    with open(path) as f:
        inputlist = eval(f.read())


def decoder(option):

    global yComponent_option1
    global  inputlist

    if option == 1:
        yComponent_option1 = inputlist
    elif option == 2:
        computeInfoOption2()

    elif option == 3:
        computeInfoOption3()

    elif option == 4:
        computeInfoOption4()

    else:
        print('Option Not Detected')


def computeInfoOption2():


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

def output(option,outputpath):

    global yComponent_option1
    global yComponent_option2
    global yComponent_option3
    global yComponent_option4

    if option == 1:
        # Output to File
        with open(outputpath, 'w') as f:
            f.write(repr(yComponent_option1))
    elif option == 2:
        # Encode
        computeInfoOption2()
        # Output to File
        with open(outputpath, 'w') as f:
            f.write(repr(yComponent_option2))
    elif option == 3:
        # Encode
        computeInfoOption3()
        # Output to File
        with open(outputpath, 'w') as f:
            f.write(repr(yComponent_option3))
    elif option == 4:
        # Encode
        computeInfoOption4()
        # Output to File
        with open(outputpath, 'w') as f:
            f.write(repr(yComponent_option4))

    print("Saved to " + outputpath)

#main
main()

