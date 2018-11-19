from picamera import PiCamera
from time import sleep

camera = PiCamera()

for i in range(5):
    sleep(0.5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()

# camera.rotation
# camera.capture('image.jpg')
