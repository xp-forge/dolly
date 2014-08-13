#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import os
import util
import project
import terminal
import dolly

class Status:
	def visit(self, host):
		for repo in host.tree:
			project.Project.currentProj += 1
			util.printStatus(repo)
			self.status(repo)
	
	def status(self, repo):
		if not os.path.exists(repo['local']):
			dolly.Dolly.not_cloned.append(repo)
			return
		if util.isGitRepo(repo):
			self.statusGit(repo)
		else:
			self.statusSvn(repo)

	def statusGit(self, repo):
		if not util.isGitCheckout(repo):
			error = "\n{0} is a Git repo in config file but not a Git checkout on disk".format(repo['local'])
			terminal.error(error)
			dolly.Dolly.warnings.append(error)
			return
		result = util.executeCommand('git status -s', cwd=repo['local'])
		for line in result['stdout'].splitlines():
			change = os.path.join(repo['local'], ' '.join(line.split()[1:]))
			dolly.Dolly.changes.append({'repo': repo, 'change': change})
		result = util.executeCommand('git status -s -b', cwd=repo['local'])
		if result['stdout']:
			if 'ahead' in result['stdout']:
				dolly.Dolly.unpushed.append(repo)


	def statusSvn(self, repo):
		if not util.isSvnCheckout(repo):
			error = "\n{0} is a Svn repo in config file but not a Svn checkout on disk".format(repo['local'])
			terminal.error(error)
			dolly.Dolly.warnings.append(error)
			return
		result = util.executeCommand('svn status', cwd=repo['local'])
		for line in result['stdout'].splitlines():
			change = os.path.join(repo['local'], ' '.join(line.split()[1:]))
			dolly.Dolly.changes.append({'repo': repo, 'change': change})