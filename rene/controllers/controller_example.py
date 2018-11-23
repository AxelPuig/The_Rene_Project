import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + '..' + os.sep + '..'
sys.path.append(dir_path)

from rene.controllers.controller import Controller

controller = Controller([22,2,3])

controller.start_example()
