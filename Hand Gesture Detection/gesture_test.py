import numpy as np
import math
import cv2
import matplotlib.pyplot as plt

skin_color = [254,195,172]
data = np.array([[skin_color for i in range(512)]for k in range(512)], dtype=np.uint8)
plt.imshow(data, interpolation='nearest')
plt.show()
