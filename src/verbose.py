from utils import *

def info(s):
    if VERBOSE:
        print(f'[ASSISTSPEC] {s}')

def err(s):
    print(f'Error: {s}')
    sys.exit(-1)

def warn(s):
    if WARNING:
        print(f'Warning: {s}')
