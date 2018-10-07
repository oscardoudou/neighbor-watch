from Logger import *

import zmq

class Daemon(Object):
	def __init__(self, ):
		pub_context = zmq.Context()
		sub_context = zmq.Context()