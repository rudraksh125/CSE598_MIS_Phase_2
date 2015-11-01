import numpy as np
import cv2
import os
import sys
from time import sleep

cap = cv2.VideoCapture('../Program-1/sampleOutputFiles/1.mp4')

while not cap.isOpened():
    cap = cv2.VideoCapture('../Program-1/sampleOutputFiles/1.mp4')
    cv2.waitKey(1000)
    print "Wait for the header"

pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
list_frames  = []

c = 0
while True and c < 250:
    c += 1
    flag, frame = cap.read()
    if flag:
        # The frame is ready and already captured
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        list_frames.append(gray)
        cv2.imshow('video', gray)
        pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        print str(pos_frame)+" frames"
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
        print "frame is not ready"
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 27:
        break
    if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break

CODEC = cv2.cv.CV_FOURCC('D','I','V','X') # MPEG-4 = MPEG-1

count=0
print "processing frames..."
for i in range(0, 250):
    if i % 10 == 0:
        print 'processed frame #:', i
    gray = list_frames[i]
    frame = cv2.cvtColor(gray, cv2.COLOR_YUV2BGR)
    f = '{:04}'.format(count)
    name = "frame"+f+".jpg"
    count+=1
    cv2.imwrite(name, frame)

# Release the capture
del(cap)
print 'released capture'

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


combine('jpg','output.mp4')
