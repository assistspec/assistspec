import os
import sys

DEBUG = True
VERBOSE = True
WARNING = True

PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_CONF = os.path.join(PATH_HOME, 'conf')

sys.path.append(PATH_CONF)
from settings import SHOW_PROOF
