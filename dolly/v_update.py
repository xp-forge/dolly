#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import os
import util
import project
import terminal
import dolly

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
		if not util.checkRemote(repo):
			error = "{0} has a different remote on disk than in config".format(repo['local'])
			terminal.error("\n" + error)
			dolly.Dolly.warnings.append(error)
		if util.isGitRepo(repo):
			self.pullGit(repo)
		else:
			self.pullSvn(repo)

	def cloneGit(self, repo):
		result = util.executeCommand('git clone {0} {1}'.format(repo['remote'], repo['local']))

	def cloneSvn(self, repo):
		result = util.executeCommand('svn checkout --config-option servers:global:store-plaintext-passwords=yes {0} {1}'.format(repo['remote'], repo['local']))

	def pullGit(self, repo):
		result = util.executeCommand('git pull --ff-only', cwd=repo['local'])

	def pullSvn(self, repo):
		result = util.executeCommand('svn update', cwd=repo['local'])