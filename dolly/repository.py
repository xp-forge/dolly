from abc import ABCMeta, abstractmethod
import os

class Repository:
	__metaclass__ = ABCMeta

	def __init__(self, repo):
		self.data = repo

	@abstractmethod
	def clone(self): pass

	@abstractmethod
	def pull(self): pass

	@abstractmethod
	def get_revision(self): pass


import util
from svnrepository import SVNRepository
from gitrepository import GitRepository

def create(repo):
	if util.isGitRepo(repo):
		return GitRepository(repo)
	else:
		return SVNRepository(repo)
