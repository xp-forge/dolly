#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import yaml
import os
import project
import dolly
import terminal
import sys

class Config:
	def __init__(self, path):
		self.data = self.__open(path)
		self.rootdir = dolly.Dolly.rootdir
	def __open(self, path):
		return yaml.load(open(path))

	def __normalizeTree(self, project):
		output = []
		for directory, repos in project.iteritems():
			for repository in repos:
				key = list(repository)[0]
				remote = repository[key]
				local = os.path.join(self.rootdir, directory, key)
				output.append({'local': local, 'remote': remote, 'name': key})
		return output

	def parse(self, name):
		if not (name in self.data):
			terminal.error("Project doesn't exist in config file")
			sys.exit(0)
		proj = self.data[name]
		tree = []
		includes = []
		description = ''
		post_update=None
		if 'tree' in proj:
			tree = self.__normalizeTree(proj['tree'])
		if 'includes' in proj:
			includes = proj['includes']
		if 'description' in proj:
			description = proj['description']
		if 'post_update' in proj:
			post_update = proj['post_update']

		return project.Project(name, description, tree, includes, self, post_update)

	def addRepo(self, remote, local, project):
		self.data[project]['tree'][os.path.relpath(os.path.abspath(os.path.join(local, '..')), self.rootdir)].append({os.path.basename(os.path.normpath(local)): remote})
		#self.data[project]['tree'][os.path.relpath(os.path.abspath(os.path.join(local, '..')), self.rootdir)][1] = remote

	def dump(self):
		print yaml.dump(self.data)

