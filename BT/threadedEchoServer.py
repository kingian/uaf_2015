import select
import socket
import sys
import threading
import argparse

host = ''
port = 50001
size = 1024

""" The main server class. """
class Server:
    def __init__(self):
        self.backlog = 5
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((host, port))
            self.server.listen(self.backlog)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        input = [self.server,sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                print s

                if s == self.server:
                    # handle the server socket
                    c = ServerClient(self.server.accept())
                    c.start()
                    self.threads.append(c)

                elif s == sys.stdin:
                    # handle standard input
                    command = sys.stdin.readline()
                    print("Received the command: %s" % command)
                    if str.strip(command) == "quit":
                        # close all threads
                        running = 0
                        continue
                    elif str.strip(command).startswith("::"):
                        print("Sending message to all clients.")
                        for t in self.threads:
                            t.sendMessageToClient(str.strip(command).strip("::"))

        self.server.close()
        for c in self.threads:
            c.join()

""" A class that represents a client on the server. """
class ServerClient(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                self.client.send(data)
            else:
                self.client.close()
                running = 0

    def sendMessageToClient(self, message):
        self.client.send(message)


""" The class that runs for on a client system."""
class Client():
    def __init__(self):
        self.keepRunning = True

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        sys.stdout.write('%')

        while self.keepRunning:
            # read from keyboard
            # may need to spawn this on a separate thread or have the listener on a separate thread. Right now it will
            # only display the message AFTER keyboard input has been received. This won't be a big deal in the real
            # client because there won't be keyboard input.
            line = sys.stdin.readline()

            # Exit client on an empty line entered.
            if line == '\n':
                self.keepRunning = False
                continue

            # send the data (message) from the command line.
            s.send(line)

            #check for more data receive queue.
            data = s.recv(size)

            sys.stdout.write(data)
            sys.stdout.write('%')
        s.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help='Starts the script in server mode.', default=False)
    args = parser.parse_args()

    # Run a server if the argument -s true or --server true
    if args.server:
        s = Server()
        s.run()
    else:
        c = Client()
        c.run()
