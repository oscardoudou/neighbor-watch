#!usr/bin/env python

import logging

class Logger(object):
	def __init__(self):
		logging.basicConfig(file='nwd.log',level = logging.DEBUG)
		self.logger = logging.getLogger()

	def do_something(self):
		self.logger.info('Initializing Neighbor Watch Daemon')