#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import project
from v_base import Visitor

class Count(Visitor):
	def visit(self, host):
		project.Project.projectCount += len(host.tree)
