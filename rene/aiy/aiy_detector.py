import argparse

from picamera import PiCamera

from vision.inference import CameraInference
from vision.models import face_detection
from vision.annotator import Annotator

def avg_joy_score(faces):
    if faces:
        return sum(face.joy_score for face in faces) / len(faces)
    return 0.0

def detect(num_frames):
    """Face detection camera inference example"""

    # Forced sensor mode, 1640x1232, full FoV. See:
    # https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
    # This is the resolution inference run on.
    with PiCamera(sensor_mode=4, resolution=(1640, 1232), framerate=30) as camera:
        camera.start_preview()

        # Annotator renders in software so use a smaller size and scale results
        # for increased performance.
        annotator = Annotator(camera, dimensions=(320, 240))
        scale_x = 320 / 1640
        scale_y = 240 / 1232

        with CameraInference(face_detection.model()) as inference:
            for result in inference.run(num_frames):
                faces = face_detection.get_faces(result)
                annotator.clear()
                for face in faces:
                    x, y, width, height = face.bounding_box
                    annotator.bounding_box((scale_x * x, scale_y * y, scale_x * (x + width),
                    scale_y * (y + height)), fill=0)
                annotator.update()

                print('#%05d (%5.2f fps): num_faces=%d, avg_joy_score=%.2f' %
                    (inference.count, inference.rate, len(faces), avg_joy_score(faces)))

        camera.stop_preview()

detect(5)