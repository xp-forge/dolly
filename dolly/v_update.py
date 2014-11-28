#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import os
import sys
import util
import project
import terminal
import signal
from multiprocessing import Pool

import dolly

def init_worker():
	# Ignore SIGINTs in worker processes.
	signal.signal(signal.SIGINT, signal.SIG_IGN)

def process_repo(upd, repo):
	upd.update(repo)

class Update:
	def visit(self, host):
		pool = Pool(5, init_worker)

		def pr(repo):
			return pool.apply_async(process_repo, (self, repo))

		results = zip(host.tree, map(pr, host.tree))

		for r in results:
			repo, result = r
			project.Project.currentProj += 1
			util.printStatus(repo)
			# Workaround to Python issue 8296 where a SIGINT will
			# lock up the process when no wait time is given.
			result.wait(9999999)

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
