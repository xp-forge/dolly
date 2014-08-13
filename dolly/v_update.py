#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import os
import util
import project

class Update:
	def visit(self, host):
		for repo in host.tree:
			project.Project.currentProj += 1
			util.printStatus(repo)
			self.update(repo)

		if host.post_update:
			util.executeCommand(host.post_update)
	
	def update(self, repo):
		if os.path.exists(repo['local']):
			self.pull(repo)
		else:
			self.clone(repo)

	def clone(self, repo):
		if util.isGitRepo(repo):
			self.cloneGit(repo)
		else:
			self.cloneSvn(repo)

	def pull(self, repo):
		if util.isGitRepo(repo):
			self.pullGit(repo)
		else:
			self.pullSvn(repo)

	def cloneGit(self, repo):
		result = util.executeCommand('git clone {0} {1}'.format(repo['remote'], repo['local']))

	def cloneSvn(self, repo):
		result = util.executeCommand('svn checkout {0} {1}'.format(repo['remote'], repo['local']))

	def pullGit(self, repo):
		result = util.executeCommand('git pull --ff-only', cwd=repo['local'])

	def pullSvn(self, repo):
		result = util.executeCommand('svn update', cwd=repo['local'])