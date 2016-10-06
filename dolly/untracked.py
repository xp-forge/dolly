import os
import os.path

import terminal
from v_base import Visitor

# Creates a set of repository paths.
class Paths(Visitor):
	def __init__(self):
		self.paths = set()

	def visit(self, host):
		for repo in host.tree:
			#project.Project.currentProj += 1
			self.add(repo)

	def add(self, repo):
		self.paths.add(os.path.abspath(repo['local']))

# Finds all untracked repositories below rootdir.
def find(rootdir, startproject):
	untracked = []
	# Build set of absolute repository paths.
	visitor = Paths()
	startproject.accept(visitor)
	paths = visitor.paths
	# Iterate over directories below rootdir.
	for root, dirs, files in os.walk(rootdir):
		# Skip subdirectories of managed projects.
		if root in paths:
			del dirs[:]
			continue
		# Detect repositories.
		if '.git' in dirs or '.svn' in dirs:
			untracked.append(root)
			# Don't recurse further.
			del dirs[:]
	return untracked

# CLI interface: Prints all untracked repositories.
def cmd(rootdir, startproject):
	dirs = find(rootdir, startproject)
	rootdir = os.path.abspath(rootdir)
	if len(dirs) == 0:
		terminal.ok('No untracked repositories.')
	else:
		terminal.warning('{0} untracked repositories below {1}:'.format(len(dirs), rootdir))
		for repo in dirs:
			repo = repo.replace(rootdir, '', 1).lstrip('/')
			print(' - {0}'.format(repo))
