#!usr/bin/env python
#track events happen when daemon runs
#
#so far we create a logger class is to ease other instantiate work when need a logger as an argument,
#you just pass a object, no need to write logging.getLogger()
import logging
#max length of log message
MAXLENGTH = 100

class Logger(object):
	def __init__(self):
		#default level is WARNING 
		FORMAT = '%(asctime)s [%(levelname)s]:%(message)s'
		logging.basicConfig(file='nwd.log', format=FORMAT, level=logging.INFO, datefmt = '%m/%d %I:%M:%S %p')
		"""
		a good convention to use when naming logger is to use  a module-level logger
		logger names track the package/module hierarchy, 
		logging.getLogger(name=None)
		return a logger with the specifed name
		if name is None, return a logger which is the root logger of the hierarchy(root)
		basically all calls to this function with a given return the same logger instance, 
		which means the logger instances never need to be passed between different parts of an app
		as long as you call this function and give a same name, it will return same logger instance
		__name__ is the module's name in python package namespace
		self.logger = logging.getLogger(__name__)
		you can use print(logging.getLogger(__name__).name) or 
		logger = Logger() print(logger.logger.name) to verify this feature.
		"""
		self.logger = logging.getLogger()
	"""
	Only for using like this logger.getLogger().info('Initializing Neighbor Watch Daemon.'),
	exposing a getLogger interface outside the class isn't a good idea. Even though you haven't expose set interface
	but still, one can log any message format any event level they want rather than use the interface you set up in this class 
	def getLogger(self):
		return self.logger
	"""
	def setLevel(self, level):
		#setLevel in logging is still a method, the one she call, _checkLevel is a function
		if level in ['debug', logging.DEBUG]:
			self.logger.setLevel(logging.DEBUG)
		elif level in ['info', logging.DEBUG]:
			self.logger.setLevel(logging.INFO)
		elif level in ['waring', 'warn', logging.WARNING]:
			self.logger.setLevel(logging.WARNING)
		elif level in ['error','err', logging.ERROR]:
			self.logger.setLevel(logging.ERROR)
		elif level in ['critical', 'crit', logging.CRITICAL]:
			self.logger.setLevel(logging.CRITICAL)
		else:
			log('error', 'Invalid log level: %s' % level)
			self.logger.setLevel(logging.DEBUG)

	def log(self, log_type, entry):
		#argument is called log_type, cause it would only show this type, different from setLevel, which enable all upper level
		output = entry

		if log_type in ['debug', 'd']:
			self.logger.debug(output[:MAXLENGTH])
		elif log_type in ['info', 'i']:
			self.logger.info(output[:MAXLENGTH])
		elif log_type in ['warning', 'warn', 'w']:
			self.logger.warning(output[:MAXLENGTH])
		elif log_type in ['error','e']:
			self.logger.error(output[:MAXLENGTH])
		elif log_type in ['critical','crit','c']:
			self.logger.critical(output[:MAXLENGTH])
		else:
			self.logger.critical('log_type %s not found', log_type)
			self.logger.critical(output[:MAXLENGTH])