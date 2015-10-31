import numpy as np
import cv2

cap = cv2.VideoCapture('../Program-1/sampleOutputFiles/1.mp4')

while not cap.isOpened():
    cap = cv2.VideoCapture('../Program-1/sampleOutputFiles/1.mp4')
    cv2.waitKey(1000)
    print "Wait for the header"

pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
list_frames  = []
outwriter = cv2.VideoWriter('output.mp4',-1, 20.0, (w,h))
c = 0
while True and c < 250:
    c += 1
    flag, frame = cap.read()
    if flag:
        #outwriter.write(frame)
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

# Initialize the video writer to write the file
# writer = cv2.cv.CreateVideoWriter(
#     'out.mp4',     # Filename
#     -1,                              # Codec for compression
#     25,                                 # Frames per second
#     (640, 480),                         # Width / Height tuple
#     False                                # Color flag
# )

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4',CODEC, 20.0, (w,h))
count=0
for i in range(0, 250):
    print 'frame #:', i
    gray = list_frames[i]
    frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    f = '{:04}'.format(count)
    name = "frame"+f+".jpg"
    count+=1
    cv2.imwrite(name, frame)
    # image = cv2.imdecode(frame, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    out.write(frame)
    # print gray
    # cv2.cv.ShowImage("w1", cv2.cv.fromarray(frame))
    # image = cv2.cv.GetImage(cv2.cv.fromarray(frame))
    # cv2.cv.WriteFrame(writer, image)


# Release the capture
del(cap)
del(out)
print 'released capture'
#
# cap = cv2.VideoCapture('out.mp4')
# while not cap.isOpened():
#     cap = cv2.VideoCapture('out.mp4')
#     cv2.waitKey(1000)
#     print "Wait for the header"
# while True:
#     flag, frame = cap.read()
#     if flag:
#         # The frame is ready and already captured
#         cv2.imshow('video', frame)
#         pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
#         print str(pos_frame)+" frames"
#
#     if cv2.waitKey(10) == 27:
#         break

