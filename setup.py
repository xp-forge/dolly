#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
from setuptools import setup
setup(
	name = 'Dolly',
	description='Dolly manages multiple git and svn repos',
	long_description=open('README.md').read(),
	packages = ['dolly'],
	version = '0.0.9',
	install_requires=['pyyaml', 'argparse'],
	entry_points={
		'console_scripts': [
			'dolly = dolly.dolly:main',
			'dly = dolly.dolly:main'
		]
	}
)