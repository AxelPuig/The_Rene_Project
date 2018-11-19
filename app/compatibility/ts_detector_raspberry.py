from __future__ import division
import cv2
import time
import sys

box_color = (255, 255, 255)
frame_process_size = (300,300)
conf_threshold = .75

modelFile = "models\\opencv_face_detector_uint8.pb"
configFile = "models\\opencv_face_detector.pbtxt"
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

def process(frame):
    """Returns the boxes list of detected faces in the @frame"""
    global net
    out_frame = frame.copy()
    height = out_frame.shape[0]
    width = out_frame.shape[1]
    #We shrink the image down to size @frame_process_size
    blob = cv2.dnn.blobFromImage(out_frame, 1.0, frame_process_size, [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:   #Definition of the left-top and right-bottom corners
            x1 = int(detections[0, 0, i, 3] * width)
            y1 = int(detections[0, 0, i, 4] * height)
            x2 = int(detections[0, 0, i, 5] * width)
            y2 = int(detections[0, 0, i, 6] * height)
            cv2.rectangle(out_frame, (x1, y1), (x2, y2), box_color, 2, 8)
            cv2.rectangle(out_frame, (x1, y1), (int(x1 + 3*(x2-x1)/6), int(y1 + (y2-y1)/10)), box_color, -1000, 8)
            cv2.putText(out_frame, str((confidence//0.0001)/100)+'%', (int(x1+(x2-x1)/20),int(y1 + (y2-y1)/12)), cv2.FONT_HERSHEY_SIMPLEX, (x2-x1)/300., (0, 0, 255-((confidence-0.75)/0.75)*255),2)
    return out_frame

def detect():
    """Detects faces present in the video source and save video to file"""
    source = 0
    #By default we use 0 but we never know if there's any camera added to device, use it
    if len(sys.argv) > 1:
        source = sys.argv[1]

    cap = cv2.VideoCapture(source)
    #has_frame, frame = cap.read()

    #vid_writer = cv2.VideoWriter('video-save-{}.avi'.format(str(source).split(".")[0]), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (frame.shape[1], frame.shape[0]))

    frame_count = 0
    tt = 0
    while (1):
        has_frame, frame = cap.read()
        if not has_frame:
            break
        frame_count += 1

        t = time.time()
        out_frame = process(frame)
        tt += time.time() - t
        fps = frame_count / tt
        label = "FPS : {:.2f}".format(fps)
        cv2.putText(out_frame, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

        cv2.imshow("Face detection using TensorFlow", out_frame)

        #vid_writer.write(out_frame)
        if frame_count == 1:
            tt = 0

        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()
    #vid_writer.release()

detect()

