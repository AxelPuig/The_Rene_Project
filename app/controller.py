import cv2
import app.detectors.detector as dt

# init the camera rotation around x,y,z, defining x pointing towards view's center and z pointing up
rotation = [0, 0, 0]

# define max angles the camera can handle around each axis (we don't rotate camera around x)
max_angles = [0, 90, 90]

detector = dt.Detector(.7, dt.FACE_DETECTION, path_to_models="detectors\\")

while True:
    out_frame, faces = detector.next_frame(data_on_frame=True, show_frame=True)
    if cv2.waitKey(1) != -1:
        break

detector.close_window()