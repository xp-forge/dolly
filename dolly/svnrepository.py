from repository import Repository
import util

class SVNRepository(Repository):
	def __init__(self, repo):
		super(GitRepository, self).__init__(repo)

	def clone(self):
		return util.executeCommand("svn checkout --config-option servers:global:store-plaintext-passwords=yes '{0}' '{1}'".format(repo['remote'], repo['local']))

	def pull(self):
		return util.executeCommand('svn update', cwd=repo['local'])
