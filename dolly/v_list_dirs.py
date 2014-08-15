#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import project

class ListDirs:
	def visit(self, host):
		for repo in host.tree:
			project.Project.currentProj += 1
			self.list(repo)

	def list(self, repo):
		print repo['local']