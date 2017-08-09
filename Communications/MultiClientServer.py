"""
This class represents a TCP server which can take multiple clients. TCPServer saves an additional dictionary to record
all the connected clients. The keys are the ip address of the client, and the values are tuples of (connection, receive
_message_queue, send_message_queue)

Be sure to run accept_clients method after construction (preferably in a newly created thread)

If connection is unsuccessful, be sure to check the firewall settings (especially if Mcafee is installed, check if
public network connection is disabled)
"""
import socket
import sys
import Queue
from Utility.Decorators import threaded # for running method in new thread


class TCPServer(object):

    def __init__(self, port, buf=1024, verbose=True):
        """
        Initialize a TCP Server object and the client dictionary
        :param port: port number
        :param buf: the buffer size to send/receive messages (default to 1024 bytes)
        """
        self.port = port
        self.buf = buf
        self.addr = ('', self.port)
        self.verbose = verbose
        # TCP socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print "Error: could not create socket!"
            sys.exit(0)
        # bind
        self.socket.bind(self.addr)
        self.socket.listen(3)
        print "Server established!"
        # keep a dictionary whose keys are client_addr and values are type of (connection, receive_queue, send_queue)
        self.clients = dict()
        # start accepting
        self.__accept_clients__()

    def receive_msg(self, client):
        return self.clients[client][1].get()

    def send_msg(self, client, msg):
        self.clients[client][2].put(msg)

    def num_conns(self):
        return len(self.clients.keys())

    @threaded
    def __start_receive_from_queue__(self, client):
        while True:
            conn = self.clients[client][0]
            message = str(conn.recv(self.buf))
            # receive queue
            self.clients[client][1].put(message)
            if self.verbose:
                print "received message: " + message
            if message == "exit":
                self.socket.close()

    @threaded
    def __start_send_to_queue__(self, client):
        while True:
            conn = self.clients[client][0]
            message_to_send = self.clients[client][2].get()
            if self.verbose:
                print "Sending... ", message_to_send
            conn.sendall(message_to_send)

    @threaded
    def __accept_clients__(self):
        """
        Start listening and accepting new clients.
        :return: none
        """
        while True:
            conn, client_addr = self.socket.accept()
            if type(client_addr) is tuple:
                client_addr = client_addr[0]
            # create a new entry in the client dictonary, first check if the key already exists or not
            if client_addr in self.clients:
                print "Error: same client is trying to connect again!"
                sys.exit(0)
            print "Client from %s is now connected with server!" % str(client_addr)
            # when one client connects, create the receive queue from this client, and the send queue to this client
            self.clients[client_addr] = (conn, Queue.Queue(), Queue.Queue())
            assert len(self.clients[client_addr]) == 3
            # create threads for send/receive of this client
            self.__start_receive_from_queue__(client_addr)
            self.__start_send_to_queue__(client_addr)
