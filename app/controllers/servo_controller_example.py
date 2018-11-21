import app.controllers.servo_controller as sct
import time

sct.setup_GPIO()
controller = sct.ServoController(2)
time.sleep(1)
controller.set_percent(1)
time.sleep(3)
controller.set_percent(0)
time.sleep(1)
sct.clear()