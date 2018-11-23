import os
import sys
import platform

if platform.uname()[1] != "raspberrypi":
    raise SystemError("This code must be run on raspberry")

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + '..')
import rene.controller.servo_controller as sct
import time

sct.setup_GPIO()
controller = sct.ServoController(3)
time.sleep(1)
controller.set_ratio(1)
time.sleep(3)
controller.set_ratio(0)
time.sleep(1)
sct.clear()
