#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import os
import util
import project
import v_update

# Install is like update, but doesn't perform pulls.
class Install(v_update.Update):
	def __init__(self, run_post_update):
		super(Install, self).__init__(run_post_update)

	def impl(self):
		return InstallImpl(self.run_post_update)

class InstallImpl(v_update.UpdateImpl):
	def __init__(self, run_post_update):
		super(InstallImpl, self).__init__(run_post_update)

	def pull(self, repo):
		return
