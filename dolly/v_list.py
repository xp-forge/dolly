#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import project

class List:
	def visit(self, host):
		for repo in host.tree:
			project.Project.currentProj += 1
			self.list(repo)

	def list(self, repo):
		print '({3}/{4}) [{0}] {1} => {2}'.format(repo['name'], repo['remote'], repo['local'], project.Project.currentProj, project.Project.projectCount)