#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
class Project:
	projectCount = 0
	projects = []
	currentProj = 0

	def __init__(self, name, description, tree, includes, config, post_update=None):
		self.name = name
		self.description = description
		self.tree = tree
		self.includes = includes
		self.config = config
		
		self.post_update = post_update

	def accept(self, visitor):
		
		Project.projects.append(self.name)
		for include in self.includes:
			if not include in Project.projects:
				subproj = self.config.parse(include)
				subproj.accept(visitor)

		visitor.visit(self)