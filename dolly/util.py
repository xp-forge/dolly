#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
import subprocess
import project
import dolly
import terminal
import sys
import os
import time

def isGitRepo(repo):
	return repo['remote'].endswith('.git')

def isSvnCheckout(repo):
    return os.path.exists(repo['local'] + '/.svn')

def isGitCheckout(repo):
    return os.path.exists(repo['local'] + '/.git')

def executeTmuxCommand(command, cwd='.', name=None):
	def red(msg):
		return '\033[91m{0}\033[0m'.format(msg)
	def blue(msg):
		return '\033[94m{0}\033[0m'.format(msg)
	context = '[{0}] '.format(name) if name != None else ''
	on_error = red('{0}Command failed, press enter to close'.format(context))
	# Build the actual command which will be passed to tmux. In the usual case,
	# the command runs through and the window closes. The ERR trap handles
	# failing commands and shows a message, keeping the window open. We have to
	# duplicate backslashes to make sure escapes are not interpreted too early.
	# TODO: Duplicating backslashes is probably not enough for all cases.
	cmd = "trap 'echo -n \"{0}\"; read; exit' ERR; echo \"{1}\"; {2}".format(on_error, blue(context), command.replace('\\', '\\\\'))
	pane = subprocess.check_output(['tmux', 'split-window', '-Pbd', '-F#{pane_id}', '-l2', '-t{0}'.format(os.getenv('TMUX_PANE', '')), '-c{0}'.format(cwd), cmd])
	# Poll for completion.
	while subprocess.check_output(['tmux', 'list-panes', '-a', '-F#{pane_id}']).find(pane) != -1:
		time.sleep(0.1)
	# Nothing is captured, but output/stderr are both visible anyways.
	return {'returncode': 0, 'stdout': '', 'stderr': ''}

def executeCommand(command, cwd=None, tmux=False, name=None):
	if tmux and os.getenv('TMUX') != None:
		# We seem to be inside a tmux window, so try using a tmux split
		# instead. If this turns out to be wrong or doesn't work for some other
		# reason, fall back to the usual execution.
		try:
			return executeTmuxCommand(command, cwd, name)
		except subprocess.CalledProcessError:
			pass

	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, bufsize=0)
	output = ''
	if dolly.Dolly.verbose:
		print ''
		for line in iter(proc.stdout.readline, ''):
			sys.stdout.write(line)
			output += line
	stdout, stderr = proc.communicate()
	output += stdout
	returncode = proc.returncode
	if not returncode == 0:
		print ''
		terminal.error('Error while executing command "{0}"'.format(command))
		terminal.error(output)
		terminal.error(stderr)
		dolly.Dolly.warnings.append('Error while executing command "{0}" in "{1}"'.format(command, cwd))
	return {'returncode': returncode, 'stdout': output, 'stderr': stderr}


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
