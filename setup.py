#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
from setuptools import setup
setup(
	name = 'Dolly',
	packages = ['dolly'],
	version = '0.0.2',
	install_requires=['pyyaml', 'argparse'],
	entry_points="""
	[console_scripts]
	dolly = dolly.__main__
	dly = dolly.__main__
	dollz = dolly.__main__
	dlz = dolly.__main__
	"""
)