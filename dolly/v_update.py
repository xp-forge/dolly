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
from v_base import Visitor

def init_worker():
	# Ignore SIGINTs in worker processes.
	signal.signal(signal.SIGINT, signal.SIG_IGN)

def process_repo(upd, repo):
	upd.update(repo)

# Visitor for updating repositories.
#
# Quick overview of parallelism:
#  - Projects are processed sequentially.
#  - Repositories within a project are updated in parallel. This includes
#    execution of post_update commands.
#  - Project-level post_update commands are run in parallel.
class Update(Visitor):
	def __init__(self, run_post_update = True):
		self.run_post_update = run_post_update
		if run_post_update:
			self.post_update_pool = Pool(3, init_worker)
		self.impl = self.impl()

	def impl(self):
		return UpdateImpl(self.run_post_update)

	def visit(self, host):
		pool = Pool(5, init_worker)

		def pr(repo):
			return pool.apply_async(process_repo, (self.impl, repo))

		results = zip(host.tree, map(pr, host.tree))

		for r in results:
			repo, result = r
			project.Project.currentProj += 1
			util.printStatus(repo)
			# Workaround to Python issue 8296 where a SIGINT will
			# lock up the process when no wait time is given.
			result.wait(9999999)

		if host.post_update and self.run_post_update:
			self.post_update_pool.apply_async(util.executeCommand, (host.post_update, dolly.Dolly.rootdir))

	def close(self):
		if self.run_post_update:
			self.post_update_pool.close()
			self.post_update_pool.join()
	
# Separated as Pools can't be moved to subprocesses.
class UpdateImpl(object):
	def __init__(self, run_post_update):
		self.run_post_update = run_post_update

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
		if not util.checkRemote(repo.data):
			error = "{0} has a different remote on disk than in config".format(repo.data['local'])
			terminal.error("\n" + error)
			dolly.Dolly.warnings.append(error)

		revision = repo.get_revision()
		result = repo.pull()

		# Only run post-update commands when the repository's revision
		# was updated.
		if result['returncode'] == 0 and revision != repo.get_revision():
			self.runPostUpdateCommand(repo)



	def runPostUpdateCommand(self, repo):
		repo = repo.data
		if repo['post_update'] != '' and self.run_post_update:
			util.executeCommand(repo['post_update'], cwd=repo['local'])
