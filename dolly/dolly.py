#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import argparse
import v_list
import v_count
import v_update
import v_status
import config
import os
import sys
import project
import terminal
import util

class Dolly:
	verbose = False
	rootdir = None
	not_cloned = []
	unpushed = []
	changes = []

	def __init__(self):
		parser = argparse.ArgumentParser()
		parser.add_argument("command", help="Status/Update/List")
		parser.add_argument("project", help="The project to execute the command on", default="default", nargs="?")
		parser.add_argument("-v", "--verbose", action="store_true", help="Verbose Output")
		parser.add_argument("-r", "--rootdir", help="Clone repos relative to this path", default=os.path.expanduser('~/dev'))
		parser.add_argument("-c", "--config", help="Specify your dolly.yml")
 
		self.args = parser.parse_args()
		Dolly.verbose = self.args.verbose
		Dolly.rootdir = self.args.rootdir
		self.startproject = None

	def run(self):
		config_system = '/etc/dolly/dolly.yml'
		config_user = os.path.expanduser('~/.dolly.yml')
		if self.args.config:
			self.config=self.args.config
		elif os.path.exists(config_user):
			self.config = config_user
		elif os.path.exists(config_system):
			self.config = config_system
		else:
			terminal.error('No valid config file found')
			return
		parser = config.Config(self.config)
		self.startproject = parser.parse(self.args.project)
		self.countProjects()
		self.run_visitor()
		

	def run_visitor(self):
		command = self.args.command
		visitor = None
		if command in ['status', 'st']:
			visitor = v_status.Status()
		elif command in ['update', 'up']:
			visitor = v_update.Update()
		elif command in ['list', 'lst']:
			visitor = v_list.List()
		else:
			print 'Invalid command'
			sys.exit(0);
		self.startproject.accept(visitor)
		self.printSummary()

	def countProjects(self):
		counter = v_count.Count()
		self.startproject.accept(counter)
		project.Project.projects = []

	def printSummary(self):
		if self.args.command in ['status', 'st']:
			print '\n'
			terminal.blue('---SUMMARY---')
			print ''
			if len(Dolly.not_cloned) > 0:
				terminal.warning('The following repositories were not cloned')
				for repo in Dolly.not_cloned:
					util.printStatus(repo, False)
			print ''
			if len(Dolly.unpushed) > 0:
				terminal.warning('The following repositories contain unpushed commits')
				for repo in Dolly.unpushed:
					util.printStatus(repo, False)
			else:
				terminal.ok('No unpushed commits')
			print ''
			if len(Dolly.changes) > 0:
				terminal.warning('The following repositories contain uncomitted changes')
				for change in Dolly.changes:
					print '[{0}] {1}'.format(change['repo']['name'], change['change'])
			else:
				terminal.ok('No uncomitted changes')

