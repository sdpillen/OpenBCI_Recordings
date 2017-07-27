"""
This class represents a TCP server which can send and receive messages from a TCP Client

If connection is unsuccessful, be sure to check the firewall settings (especially if Mcafee is installed, check if
public network connection is disabled)
"""
import socket
import sys


class TCPServer(object):

    def __init__(self, port, buf=1024):
        """Initialize a TCP Server object and wait for clients to connect
        :param port: port number
        :param receive_message_queue: the queue to receive messages from (client)
        :param send_message_queue: the queue to send messages to (client)
        :param buf: the buffer size to send/receive messages (default to 1024 bytes)
        """
        self.port = port
        self.buf = buf
        self.addr = ('', self.port)
        # TCP socket
        try:
            self.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print "Error: could not create socket!"
            sys.exit(0)
        # bind
        self.socket.bind(self.addr)
        self.socket.listen(3)
        # keep a dictionary whose keys are client_addr and values are type of (connection, receive_queue, send_queue)
        self.clients = dict()

    def accept_clients(self, receive_message_queue, send_message_queue):
        # should be called in a new thread!
        while True:
            conn, client_addr = self.socket.accept()
            # create a new entry in the client dictionary, first check if the key already exists or not
            if client_addr in self.clients:
                print "Error: same client is trying to connect again!"
                sys.exit(0)
            print "Client from: %s is now connected with server!" % str(client_addr)
            self.clients[client_addr] = (conn, receive_message_queue, send_message_queue)
            assert len(self.clients[client_addr]) == 3

    def start_receive_from_queue(self, client_addr):
        while True:
            conn = self.clients[client_addr][0]
            message = str(conn.recv(self.buf))
            self.clients[client_addr][1].put(message)
            print "received message: " + message
            if message == "exit":
                self.socket.close()

    def start_send_to_queue(self, client_addr):
        while True:
            conn = self.clients[client_addr][0]
            message_to_send = self.clients[client_addr][1].get()
            print "Sending... ", message_to_send
            conn.sendall(message_to_send)
