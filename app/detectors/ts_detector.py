import face_recognition as fr
import imutils
import cv2
import time
import sys

frame_process_size = [(192,108), (256,144), (320,180), (300,300), (426,240), (640,360), (1280,720)][3]
conf_threshold = .2

# load our serialized face detector from disk
#model_file = "models\\opencv_face_detector_uint8.pb"
#config_file = "models\\opencv_face_detector.pbtxt"
#net = cv2.dnn.readNetFromTensorflow(model_file, config_file)

# this net is more centered
proto_txt = "models\\deploy.prototxt.txt"
model_file = "models\\res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(proto_txt, model_file)

def process(frame):
    """returns a copy of @frame where faces or shown"""
    out_frame = frame.copy()
    height = out_frame.shape[0]
    width = out_frame.shape[1]
    #We shrink the image down to size @frame_process_size
    blob = cv2.dnn.blobFromImage(out_frame, 1.0, frame_process_size, [104, 117, 123], False, False)
    #blob = imutils.resize(out_frame, width=frame_process_size[0], height=frame_process_size[1])
    net.setInput(blob)
    detections = net.forward()
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        ratio = (confidence-conf_threshold)/(1-conf_threshold)
        if confidence > conf_threshold:   # definition of the left-top and right-bottom corners
            x1 = int(detections[0, 0, i, 3] * width)
            y1 = int(detections[0, 0, i, 4] * height)
            x2 = int(detections[0, 0, i, 5] * width)
            y2 = int(detections[0, 0, i, 6] * height)
            box_color = (0, 255*ratio, 255*(1-ratio))
            if confidence < conf_threshold:
                box_color = (0, 0, 255)
            cv2.rectangle(out_frame, (x1, y1), (x2, y2), box_color, 2, 8)
            cv2.rectangle(out_frame, (x1, int(y1 + (y1-y2)/8)), (int(x1 + 2*(x2-x1)/3), y1), box_color, -1, 8)
            cv2.putText(out_frame, str((confidence//0.0001)/100)+'%', (int(x1 + (x2-x1)/20), int(y1 + (y1-y2)/40)), cv2.FONT_HERSHEY_DUPLEX, (y2-y1)/300., (255,255,255), 1)
    return out_frame

def process_fr(frame):
    """returns a copy of @frame where faces or shown"""
    global net
    out_frame = frame.copy()
    height = out_frame.shape[0]
    width = out_frame.shape[1]
    sm_image = imutils.resize(out_frame, height=frame_process_size[1], width=frame_process_size[0])
    rgb_image = cv2.cvtColor(sm_image, cv2.COLOR_BGR2RGB)
    boxes = fr.face_locations(rgb_image, model='hog')

    for i in range(len(boxes)):
        y1,x2,y2,x1 = boxes[i]
        y1 *= height/frame_process_size[1]
        y2 *= height/frame_process_size[1]
        x1 *= width/frame_process_size[0]
        x2 *= width/frame_process_size[0]
        box_color = (0, 255, 0)
        cv2.rectangle(out_frame, (int(x1), int(y1)), (int(x2), int(y2)), box_color, 2, 8)
    return out_frame

def detect():
    """Detects faces present in the video source and saves the video to file"""

    source = 0
    #By default we use 0 but we never know if there's any camera added to device, use it
    if len(sys.argv) > 1:
        source = sys.argv[1]

    print("[INFO] started camera...")

    cap = cv2.VideoCapture(source)
    #has_frame, frame = cap.read()

    #vid_writer = cv2.VideoWriter('video-save-{}.avi'.format(str(source).split(".")[0]), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (frame.shape[1], frame.shape[0]))

    frame_count = 0
    tt = 0
    while True:
        has_frame, frame = cap.read()
        if not has_frame:
            break
        frame_count += 1

        t = time.time()
        out_frame = process(frame)
        tt += time.time() - t
        fps = frame_count / tt
        label = "FPS : {:.2f}".format(fps)
        cv2.putText(out_frame, label, (5, 20), cv2.FONT_HERSHEY_DUPLEX, .4, (255, 255, 255), 1)

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