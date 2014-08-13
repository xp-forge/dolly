import os
import sys
import time

def clear_line():
  _, columns = os.popen('stty size', 'r').read().split()
  width = int(columns) - 2
  sys.stdout.write('\r')
  for i in range(1, width):
    sys.stdout.write(' ')
  sys.stdout.write('\r')
  sys.stdout.flush()

def progress_bar(pmax, val, width, append):
  sys.stdout.write('[{0}/{1}] - ['.format(val, pmax))
  sharps = int((float(val) / float(pmax)) * width)
  for i in range(0, sharps):
    sys.stdout.write('#')
  for i in range (sharps, width):
    sys.stdout.write(' ')
  percent = int((float(val) / float(pmax)) * 100)
  sys.stdout.write('] - {0}% - {1}'.format(percent, append))
  sys.stdout.flush()

def ok(message):
  print '\033[92m' + message + '\033[0m'

def error(message):
  print '\033[91m' + message + '\033[0m'

def warning(message):
  print '\033[93m' + message + '\033[0m'

def blue(message):
  print '\033[94m' + message + '\033[0m'

def purple(message):
  print '\033[95m' + message + '\033[0m'
