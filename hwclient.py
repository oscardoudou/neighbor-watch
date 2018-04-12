import zmq
import time

context = zmq.Context()
print "connecting to hwserver"
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5678")

for request in range(1,10):
	print "Sening request ", request, "..."
	socket.send("hello")

	message = socket.recv();
	print "received reply: ", request, "[", message, "]"