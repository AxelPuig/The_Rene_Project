import servo_controller as sct
import time

sct.setup_GPIO()
servo_y = sct.ServoController(3)
servo_z = sct.ServoController(2)
time.sleep(1)
for i in range(100):
    servo_y.add_ratio(0.01)
    time.sleep(0.01)
servo_y.set_ratio(1)
time.sleep(1)
servo_z.set_ratio(1)
time.sleep(2)
servo_y.set_ratio(0)
time.sleep(1)
servo_z.set_ratio(0)
time.sleep(1)
sct.clear()
