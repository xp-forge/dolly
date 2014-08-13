#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
from setuptools import setup
setup(
	name = 'Dolly',
	packages = ['dolly'],
	version = '0.0.3',
	install_requires=['pyyaml', 'argparse'],
	entry_points={
		'console_scripts': [
			'dolly = dolly.dolly:main',
			'dly = dolly.dolly:main'
		]
	}
)