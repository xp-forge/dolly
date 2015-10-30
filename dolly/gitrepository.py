from repository import Repository
import util

import os, errno

# Tries to create parent directories, avoiding race conditions.
#
# Git will do this automatically, but will fail when the directories are
# created in parallel.
def create_parent_directories(path):
	dir = os.path.dirname(path)
	if not os.path.exists(dir):
		try:
			os.makedirs(dir)
		except OSError, e:
			# We could check e.errno here for errno.EEXIST, but git will fail for all other errors anyways.
			return

class GitRepository(Repository):
	def __init__(self, repo):
		super(GitRepository, self).__init__(repo)

	def clone(self):
		repo = self.data
		create_parent_directories(repo['local'])
		branch = repo['branch']
		if repo['tag'] != '':
			branch = repo['tag']
		if branch != '':
			 result = util.executeCommand("git clone --branch '{2}' '{0}' '{1}'".format(
				 repo['remote'],
				 repo['local'],
				 branch
			 ))
		else:
			result = util.executeCommand("git clone '{0}' '{1}'".format(repo['remote'], repo['local']))
		return result

	def pull(self):
		repo = self.data
		if repo['tag'] != '':
			result = util.executeCommand("git checkout '{0}'".format(repo['tag']), cwd=repo['local'])
		else:
			result = util.executeCommand('git pull --ff-only', cwd=repo['local'])
		return result

	def get_revision(self):
		repo = self.data
		result = util.executeCommand('git rev-parse HEAD', cwd=repo['local'])
		if result['returncode'] == 0:
			return result['stdout']
		else:
			return None
