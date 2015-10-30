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
import repository

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
		r = repository.create(repo)
		if os.path.exists(repo['local']):
			self.pull(r)
		else:
			self.clone(r)

	def clone(self, repo):
		result = repo.clone()
		if result['returncode'] == 0:
			self.runPostUpdateCommand(repo)

	def pull(self, repo):
		if not util.checkRemote(repo.repo):
			error = "{0} has a different remote on disk than in config".format(repo.repo['local'])
			terminal.error("\n" + error)
			dolly.Dolly.warnings.append(error)

		result = repo.pull()
		# TODO: Condition is wrong.
		if result['returncode'] == 0 and 'Fast-forward' in result['stdout']:
			self.runPostUpdateCommand(repo)



	def runPostUpdateCommand(self, repo):
		if repo['post_update'] != '':
			util.executeCommand(repo['post_update'], cwd=repo['local'])
