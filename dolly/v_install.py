#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import os
import util
import project

class Install:
	def visit(self, host):
		for repo in host.tree:
			project.Project.currentProj += 1
			util.printStatus(repo)
			self.update(repo)

		if host.post_update:
			util.executeCommand(host.post_update)
	
	def update(self, repo):
		if not os.path.exists(repo['local']):
			self.clone(repo)

	def clone(self, repo):
		if util.isGitRepo(repo):
			self.cloneGit(repo)
		else:
			self.cloneSvn(repo)

	def cloneGit(self, repo):
		result = util.executeCommand('git clone {0} {1}'.format(repo['remote'], repo['local']))

	def cloneSvn(self, repo):
		result = util.executeCommand('svn checkout --config-option servers:global:store-plaintext-passwords=yes {0} {1}'.format(repo['remote'], repo['local']))