__author__ = 'ysun138'

import cv2
import numpy as np
import re

def decode(compression_option, input_dc_file, output_file):
    fframe = []
    count = 0
    # with open('../Program-4/2_1_1_1.spv') as f:
    with open(input_dc_file) as f:
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
    print fframe.__len__()
    for frame_index in range(0, fframe.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                mat[frame_index,i,j] = fframe[frame_index][i][j][0]

    original_mat =   np.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
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
        np.savetxt(outfile, frame, fmt='%-7.2f')
        frame_index+=1

def distortion(original_filename, input_dc_file):
    fframe = []
    with open(original_filename) as f:
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

    exact_original_mat = np.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
    print fframe.__len__()
    for frame_index in range(0, fframe.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                exact_original_mat[frame_index,i,j] = fframe[frame_index][i][j][0]

    fframe = []
    with open(input_dc_file) as f:
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
    print fframe.__len__()
    for frame_index in range(0, fframe.__len__()):
        for i in range(0, 10):
            for j in range(0, 10):
                mat[frame_index,i,j] = fframe[frame_index][i][j][0]

    original_mat = np.ndarray((fframe.__len__(),10,10), dtype = float, order = 'F')
    frame_index = 0
    compression_option = int(input_dc_file.split("_")[1])
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
        print (p_signal/p_noise)
def main():
    # option = 5
    # decode(option, "2_5_1_2_dc.spv", "test")
    distortion("2_original.spc", "2_5_1_2_dc.spv")

if __name__ == '__main__':
    main()