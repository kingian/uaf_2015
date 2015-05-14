import select
import socket
import sys
import threading
import thread
import argparse

host = ''
port = 50000
size = 1024

""" The main server class. """
class Server:
    def __init__(self):
        self.backlog = 5
        self.server = None
        self.threads = []
        self.serverRunning = True

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

    def close_client(self, sock):
        for client in self.threads:
            if client.is_socket(sock):
                self.threads.remove(client)
                client.close()
                print("Client disconnected.")

    def run(self):
        self.open_socket()
        inputs = [self.server, sys.stdin]

        while self.serverRunning:
            try:
                input_ready, output_ready, except_ready = select.select(inputs, self.threads, [])
            except select.error, err:
                break
            except socket.error, err:
                # for socket_output in output_ready:
                #     print("Client disconnected.")
                #     socket_output.close()
                break

            for sock in input_ready:
                if sock == self.server:
                    # handle the server client socket
                    client = ServerClient(self.server.accept())
                    client.start()
                    self.threads.append(client)

                elif sock == sys.stdin:
                    # handle input from the console.
                    command = sys.stdin.readline()
                    if str.strip(command).startswith("::"):
                        if str.strip(command) == "quit":
                            # close all threads
                            self.serverRunning = False
                            continue
                    else:
                        print("Sending message to all clients.")
                        for t in self.threads:
                            t.send_message_to_client(str.strip(command))
                else:
                    print("Some message...")

        self.server.close()
        for client in self.threads:
            client.close()
            client.join()

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

    def send_message_to_client(self, message):
        self.client.send(message)

    def close(self):
        self.client.close()

    def is_socket(self, sock):
        return self.client == sock

    def fileno(self):
        return self.client.fileno()


""" The class that runs on a client system."""
class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keepRunning = True

    def run(self):
        self.socket.connect((host, port))

        try:
            child_thread_server_listener = threading.Thread(target=self.server_listener())
            child_thread_server_listener.start()

            # child_thread_keyboard_listener = threading.Thread(target=self.keyboard_listener())
            # child_thread_keyboard_listener.start()

            # join the threads to wait for all of them to finish.
            # child_thread_keyboard_listener.join()
            child_thread_server_listener.join()

            # serverListenerThread = thread.start_new_thread(self.server_listener())
            # keyboardListenerThread = thread.start_new_thread(self.keyboard_listener())
        except KeyboardInterrupt:
            print("\nClosing the connection")

        self.socket.close()

    def server_listener(self):
        print("Server listener active:")

        while self.keepRunning:
            # check for more data receive queue.
            data = self.socket.recv(size)
            sys.stdout.write("Received: %s\n" % data)
            sys.stdout.flush()

    def keyboard_listener(self):
        print("Keyboard listener active")
        while self.keepRunning:
            sys.stdout.write('% ')

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
            self.socket.send(line)



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
