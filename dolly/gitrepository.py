from repository import Repository
import util

class GitRepository(Repository):
	def __init__(self, repo):
		super(GitRepository, self).__init__(repo)

	def clone(self):
		repo = self.repo
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
		if repo['tag'] != '':
			result = util.executeCommand("git checkout '{0}'".format(repo['tag']), cwd=repo['local'])
		else:
			result = util.executeCommand('git pull --ff-only', cwd=repo['local'])
		return result
