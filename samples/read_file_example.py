import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + '..'
sys.path.append(dir_path)
from rene.talker import read_file

read_file(dir_path + "rene/talker/hey")

