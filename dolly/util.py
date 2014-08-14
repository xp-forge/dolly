#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import subprocess
import project
import dolly
import terminal
import sys
import os

def isGitRepo(repo):
	return repo['remote'].endswith('.git')

def isSvnCheckout(repo):
    return os.path.exists(repo['local'] + '/.svn')

def isGitCheckout(repo):
    return os.path.exists(repo['local'] + '/.git')

def executeCommand(command, cwd=None):
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, bufsize=0)
	if dolly.Dolly.verbose:
		print ''
		for line in iter(proc.stdout.readline, ''):
			sys.stdout.write(line)
	stdout, stderr = proc.communicate()
	returncode = proc.returncode
	if not returncode == 0:
		print ''
		terminal.error('Error while executing command "{0}"'.format(command))
		terminal.error(stdout)
		terminal.error(stderr)
	return {'returncode': returncode, 'stdout': stdout, 'stderr': stderr}


def printStatus(repo, count=True):
	if dolly.Dolly.verbose or count==False:
		if count:
			print ''
			print '({3}/{4}) [{0}] {1} => {2}'.format(repo['name'], repo['remote'], repo['local'], project.Project.currentProj, project.Project.projectCount)
		else:
			print '[{0}] {1} => {2}'.format(repo['name'], repo['remote'], repo['local'])
	else:
		terminal.clear_line()
		terminal.progress_bar(project.Project.projectCount, project.Project.currentProj, 30, repo['name'])

def checkRemote(repo):
	command = ''
	if isGitCheckout(repo):
		command = 'git remote -v'
	else:
		command = 'svn info '
	result = executeCommand(command, cwd=repo['local'])
	return (repo['remote'] in result['stdout']) or (result['returncode'] != 0)
