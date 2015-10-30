from repository import Repository
import util

class SVNRepository(Repository):
	def __init__(self, repo):
		super(SVNRepository, self).__init__(repo)

	def clone(self):
		repo = self.data
		return util.executeCommand("svn checkout --config-option servers:global:store-plaintext-passwords=yes '{0}' '{1}'".format(repo['remote'], repo['local']))

	def pull(self):
		repo = self.data
		return util.executeCommand('svn update', cwd=repo['local'])

	def get_revision(self):
		repo = self.data
		result = util.executeCommand('svnversion', cwd=repo['local'])
		if result['returncode'] == 0:
			return result['stdout']
		else:
			return None
