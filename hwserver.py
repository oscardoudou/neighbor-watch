import zmq
import time

context = zmq.Context();
socket = context.socket(zmq.REP);
# * indicate all interface 
socket.bind("tcp://*:5678")

while True:
	message = socket.recv()
	print "Received request: ", message

	time.sleep(1)

	socket.send("World")