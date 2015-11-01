import pickle
import numpy
import cv2

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