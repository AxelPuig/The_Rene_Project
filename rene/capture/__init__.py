import platform
import cv2

ON_RASPBERRY = platform.uname()[1] == 'raspberrypi'

if ON_RASPBERRY:
    from picamera.array import PiRGBArray
    from picamera import PiCamera

# sensor modes as detailed in https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
sensor_modes = [(1920, 1080, 30), (3280, 2464, 15), (3280, 2464, 15), (1640, 1232, 40), (1640, 922, 40),
                (1280, 720, 90), (640, 480, 90)]

RES_HD = 0
RES_FULL_HD = 1
RES_1232 = 3
RES_922 = 4
RES_720 = 5
RES_480 = 6


class Capture():
    """
    Class managing the camera, whether it is run on raspberry or laptop.
    Use read method to get the retval and frame.
    """

    def __init__(self, source=0, sensor_mode=RES_480, frame_rate=0):
        """Initializes the camera and grab a reference to the raw camera capture and return a camera object"""

        if ON_RASPBERRY:
            width, height, max_fps = sensor_modes[sensor_mode]
            if not frame_rate:
                frame_rate = int(2 * max_fps / 3)

            self.cam = PiCamera(sensor_mode=5, resolution=(width, height), framerate=frame_rate)
        else:
            self.cap = cv2.VideoCapture(source)

    def read(self):
        """Return a frame took by the camera in a numpy array format"""

        if ON_RASPBERRY:
            raw_capture = PiRGBArray(self.cam, size=self.cam.resolution)
            self.cam.capture(raw_capture, format="bgr")
            frame = raw_capture.array
            return frame is not None, frame
        else:
            return self.cap.read()

    def get_cap(self):
        """Returns the object used to acquire frames"""

        return self.cap

    def __del__(self):
        if not ON_RASPBERRY:
            self.cap.release()
