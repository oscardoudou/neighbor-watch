import sys
import os
import configparser
from Logger import *


if __name__ == '__main__':
	logger = Logger()
	# sys.argv is a list in Python, which contains the command-line arguments passed to the script. 
	if len(sys.argv) != 2:
		print("usage: sudo python %s <path to config file>" % sys.argv[0])
		sys.exit(1)
	else:
		# The str() function converts values to a string form so they can be combined with other strings.
		config_file = sys.argv[1]

		if not os.path.isfile(config_file):
			print("Cannot open config file for parsing.")
			sys.exit(1)

		# Parse the config file
		config = configparser.ConfigParser()
		config.read(config_file)
		print logging.DEBUG
		logger.logger.debug('Initializing')
		logger.logger.info('Initializing Neighbor Watch Daemon.')
		logger.setLevel('debug')
		logger.logger.debug('This time i could see')
		logger.log('debug','This is a debug log')
		logger.log('Fuck','This should be in critical log')
		
		pub_address = config['SETTINGS']['pub_address']
		min_threshold = config['SETTINGS']['min_threshold']
		max_threshold = config['SETTINGS']['max_threshold']
		sub_address = config['SETTINGS']['sub_address']
		
		pub_port = config['SETTINGS'].getint('pub_port')
		# sub_addrs = json.loads(config['SETTINGS']['sub_address'])

		neighbor_ip_to_egress_dev = {}

		local_dev_to_local_ip = {}

		for ip in config['NEIGHBORS']:
			neighbor_ip_to_egress_dev[ip] = config['NEIGHBORS'][ip]

		for dev in config['DEVICES']:
			local_dev_to_local_ip[dev] = config['DEVICES'][dev]

		print pub_address
		print min_threshold
		print max_threshold
		print sub_address
		print pub_port

		for ip in neighbor_ip_to_egress_dev:
			print ip + " = " + neighbor_ip_to_egress_dev[ip]
		for dev in local_dev_to_local_ip:
			print dev + " = " + local_dev_to_local_ip[dev]