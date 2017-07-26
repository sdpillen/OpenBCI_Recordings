"""
This class represents a TCP server which can send and receive messages from a TCP Client

If connection is unsuccessful, be sure to check the firewall settings (especially if Mcafee is installed, check if
public network connection is disabled)
"""
import socket
import sys
import Queue
from thread import start_new_thread

class TCPServer(object):

    def __init__(self, port, receive_message_queue, send_message_queue, buf=1024):
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
            print "Could not create socket."
            sys.exit(0)
        # bind
        self.socket.bind(self.addr)
        self.socket.listen(3)
        # keep a dictionary whose keys are client_addr and values are list of two queues: receive_queue, send_queue
        self.clients = dict()


    def accept_clients(self):
        # should be called in a new thread!
        while True:
            conn, client_addr = self.socket.accept()
            # create a new entry in the client dictionary, first check if the key already exists or not
            if client_addr in self.clients:
                print "Error: same client is trying to connect again!"
                sys.exit(0)
            self.clients[(conn, client_addr)] = []
            print "Client from: %s is now connected with server!" % str(client_addr)


    def handle_client(self):
        # TODO: finish handling client
        return 0
        # accept the connection
        # self.conn, self.client_addr = self.socket.accept()
        # self.receive_message_queue = receive_message_queue
        # self.send_message_queue = send_message_queue

    def start_receive_from_queue(self):
        """Receive messages from clients and pass them to the receive_message_queue. Close the socket if the message
        received is 'exit'
        :return: none
        """
        while True:
            message = str(self.conn.recv(self.buf))
            self.receive_message_queue.put(message)
            print "received message: " + message
            if message == "exit":
                self.socket.close()

    def start_send_to_queue(self):
        """Send messages to clients and pass them to the send_message_queue.
        :return: none
        """
        while True:
            message_to_send = self.send_message_queue.get()
            print "Sending... ", message_to_send
            self.conn.sendall(message_to_send)