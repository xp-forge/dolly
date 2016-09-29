from abc import ABCMeta, abstractmethod

class Visitor(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def visit(self, host): pass

	def close(self): pass
