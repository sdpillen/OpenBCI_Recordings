"""
This class represents a TCP Client which can receive and send messages to a TCP Server

If connection is unsuccessful, be sure to check the firewall settings (especially if Mcafee is installed, check if
public network connection is disabled)
"""
from CCDLUtil.Utility.Decorators import threaded  # for running method in new thread
import socket
import Queue
import Util

class TCPClient(object):

    def __init__(self, server_ip, port, buf=1024, verbose=True):
        """Initialize a TCP Client object
        :param server_ip: the ip address of the server to connect to
        :param port: port number
        :param buf: the buffer size to send/receive messages (default to 1024 bytes)
        :param verbose: flag for printing messages
        """
        self.buf = buf
        self.ip = server_ip
        self.port = port
        self.verbose = verbose
        # try to connect to server
        self.TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPSock.connect((self.ip, self.port))

        self.send_message_queue = Queue.Queue()
        self.receive_message_queue = Queue.Queue()

        self.__start_receive_from_queue__()
        self.__start_send_to_queue__()

    def send_message(self, message):
        """
        Send message to server
        :param message: message to send
        :return: none
        """
        self.send_message_queue.put(message)

    def receive_message(self):
        """
        Receive message from server
        :return: message
        """
        return self.receive_message_queue.get()

    @threaded
    def __start_receive_from_queue__(self):
        """start receiving messages from server and pass them to the receive_message_queue
        :return: none
        """
        while True:
            received_message = self.TCPSock.recv(self.buf)
            if self.verbose: print "Server sends: " + received_message
            self.receive_message_queue.put(received_message)

    @threaded
    def __start_send_to_queue__(self):
        """start sending messages to server and pass them to the send_message_queue. Send 'exit' to close the socket
        :return: none
        """
        while True:
            message_to_send = str(self.send_message_queue.get())
            if self.verbose: print "Sending", message_to_send
            self.TCPSock.send(message_to_send)
