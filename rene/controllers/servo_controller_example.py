import servo_controller as sct
import time

sct.setup_GPIO()
controller = sct.ServoController(3)
time.sleep(1)
controller.set_ratio(1)
time.sleep(3)
controller.set_ratio(0)
time.sleep(1)
sct.clear()
