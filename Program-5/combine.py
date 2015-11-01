import pickle
import numpy
import cv2
import re

def combine_tpv():
    with open('../Program-4/1_2_1_1.tpv') as f:
        list2 = eval(f.read())

    row_length = 3
    col_length = 3

    numpy.set_printoptions(threshold='nan')
    frames=numpy.array([numpy.array(xi) for xi in list2])
    print frames

    frames = numpy.transpose(frames)
    print "transpose "
    print frames

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
                l.append(numpy.array((t)))
            else:
                t = frames[i][j],0,0
                l.append(numpy.array((t)))
        r.append(numpy.array(l))
        window.append(numpy.array(r))

    for i in range(len(window)):
        print "frame #: " + str(i)
        print window[i]

    cv2.imshow('video', window)
    print "tst"

def combine_spv():
    fframe = []
    count = 0
    # with open('../Program-4/2_1_1_1.spv') as f:
    with open('frame.spv') as f:
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
                    r.append(numpy.array(pixel))
            frames.append(numpy.array(r))
        else:
            if len(frames)>0:
                fframe.append(numpy.array(frames))
                frames = []
    fframe.append(numpy.array(frames))

    for ff in fframe:
        cv2.imshow('video', ff)
        if (cv2.waitKey(10) & 0xFF) == ord('q'): # Hit `q` to exit
            break
        f = '{:04}'.format(count)
        name = "frame"+f+".jpg"
        count+=1

        cv2.imwrite(name, ff)
    print "tst"

#main
combine_spv()