#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import project

class Count:
	def visit(self, host):
		project.Project.projectCount += len(host.tree)