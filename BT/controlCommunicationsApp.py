#!/usr/bin/env python
import select
import socket
import sys
import argparse
import traceback
from pi_cam_control import *

MAX_READ_SIZE = 1024

""" The main server class. """
class Server:
    def __init__(self, port):
        self.backlog = 5
        self.server = None
        # self.threads = []
        self.clients = [sys.stdin]
        self.serverRunning = True
        self.host = ''
        self.port = port

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)

        # add server socket object to the list of readable connections
        self.clients.append(server_socket)

        print "Chat server started on port " + str(self.port)

        while self.serverRunning:

            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read, ready_to_write, in_error = select.select(self.clients, [], [])

            for sock in ready_to_read:
                if sock == sys.stdin:
                    # stdin so we received a message from the server console.
                    data = sys.stdin.readline()
                    if data.strip().startswith(":"):
                        # Server command
                        command = data.strip('\n').strip(':')
                        if command == "quit":
                            self.broadcast(server_socket, None, "end")
                            self.serverRunning = False
                            for client in self.clients:
                                client.close()
                    else:
                        # Send server message to clients.
                        self.broadcast(server_socket, None, data)

                elif sock == server_socket:
                    # a new connection request received
                    sockfd, addr = server_socket.accept()
                    self.clients.append(sockfd)
                    print "Client (%s, %s) connected" % addr

                    self.broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

                else:
                    # a message from a client, not a new connection
                    # process data received from client,
                    try:
                        # receiving data from the socket.
                        data = sock.recv(MAX_READ_SIZE)
                        if data:
                            # there is something in the socket
                            self.broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                        else:
                            # remove the socket that's broken
                            if sock in self.clients:
                                self.clients.remove(sock)

                            # at this stage, no data means probably the connection has been broken
                            self.broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)

                            # exception
                    except socket.error, err:
                        self.broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                        continue

        server_socket.close()

    # broadcast chat messages to all connected clients
    def broadcast (self, server_socket, sock, message):
        for client in self.clients:
            # send the message only to peer
            if client != server_socket and client != sock and client != sys.stdin:
                try:
                    client.send(message)
                except socket.error, err:
                    # broken socket connection
                    client.close()
                    # broken socket, remove it
                    if client in self.clients:
                        self.clients.remove(client)

class Client:
    def __init__(self, server_addr, port):
		self.server_addr = server_addr
		self.server_port = port
		self.running = True
		self.camCon = CamControl()
		pass

    def run(self):
		
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.settimeout(2)

		# connect to remote host
		try:
			server_socket.connect((self.server_addr, self.server_port))
		except socket.error, err:
			print 'Unable to connect...'
			sys.exit()
			
		print 'Connected to server...'
			
		# configure and start camera controler
		err = ""
		try:
			err = self.camCon.getConfig('config.json')
			pids = self.camCon.startServices()
			self.motionPid = pids[0]
			self.cleanerPid = pids[1]
		except:
			print 'An error occured while starting camera controller...'
			print traceback.format_exc()
			sys.exit()	
			
		print 'Camera controller started...'
			
		sys.stdout.write('[Me] ')
		sys.stdout.flush()

		while self.running:
			socket_list = [sys.stdin, server_socket]

			# Get the list sockets which are readable
			ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

			for sock in ready_to_read:
				# Remove if & else block
				if sock == server_socket:
					# incoming message from remote server, s
					data = sock.recv(4096)
					if not data:
						print '\nDisconnected from chat server'
						self.camCon.endServices();
						sys.exit()
					else:
						print ("Incoming Data:" + data.strip('\n'))
						msg = self.camCon.evalCommand(data.strip('\n'))
						print msg
						sys.stdout.write(data)
						sys.stdout.flush()
						server_socket.send(msg)

				else:
					# user entered a message
					msg = sys.stdin.readline()
					if msg == '':
						# Stop the client.
						self.running = False
						continue

					server_socket.send(msg)
					sys.stdout.write('[Me] ')
					sys.stdout.flush()
					
					
# MAIN EXECUTION LOOP					
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server',
                        help='Server mode.',
                        action='store_true')
    parser.add_argument('-c', '--client',
                        metavar='SERVER_IP',
                        help='Client mode. Connects to the server on the specified ip address.')
    parser.add_argument('-p', '--port',
                        help='Server port number.',
                        default=50000)
    args = parser.parse_args()

    # Run a server if the argument -s true or --server true
    if args.server:
        s = Server(int(args.port))
        s.run()
    elif args.client:
        c = Client(args.client, int(args.port))
        c.run()
    else:
        parser.print_help()
