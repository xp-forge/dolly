#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 

import dolly
import sys

banner=r"""                       
     _     ,--.      |    |         
  _-(_)-   |   |,---.|    |    ,   .
`(___)     |   ||   ||    |    |   |
 // \\     `--' `---'`---'`---'`---|
                               `---'
"""

print banner

try:
	cmd = dolly.Dolly()
	cmd.run()
except KeyboardInterrupt:
	# Don't print a stacktrace.
	sys.exit(1)
