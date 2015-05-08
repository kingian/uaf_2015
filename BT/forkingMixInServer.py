#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter - 2
# This program is optimized for Python 2.7
# It may run on any other version with/without modifications.
import os
import socket
import threading
import SocketServer
import random
SERVER_HOST = 'localhost'
SERVER_PORT = 0 # tells the kernel to pick up a port dynamically
BUF_SIZE = 1024

def client(ip, port, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip,port))
	try:
		sock.sendall(message)
		response = sock.recv(BUF_SIZE)
		
		stuff = "fizz"
		
		if (response == "1"):
			stuff = "bang"
		elif (response == "2"):
			stuff = "boom"
		
		print "Client received: %s %s" %(response,stuff)
	finally:
		sock.close()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request.recv(1024)
		current_thread = threading.current_thread()
#		response = "%s: %s" %(current_thread.name, data)
		response = "%s" %str(random.randint(0,2))
		self.request.sendall(response)
		
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == "__main__":
	server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT),ThreadedTCPRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print "Server loop running on thread: %s" %server_thread.name
	#Run clients
	client(ip, port, "Hello from client 1")
	client(ip, port, "Hello from client 2")
	client(ip, port, "Hello from client 3")
	server.shutdown()