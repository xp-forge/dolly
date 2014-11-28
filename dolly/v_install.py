#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import os
import util
import project
import v_update

# Install is like update, but doesn't perform pulls.
class Install(v_update.Update):
	def pull(self, repo):
		return
