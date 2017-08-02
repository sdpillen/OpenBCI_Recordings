"""
This class represents a TCP Client which can receive and send messages to a TCP Server

If connection is unsuccessful, be sure to check the firewall settings (especially if Mcafee is installed, check if
public network connection is disabled)
"""
from threading import Thread
import socket


class TCPClient(object):

    def __init__(self, server_ip, port, receive_message_queue, send_message_queue, buf=1024):
        """Initialize a TCP Client object
        :param server_ip: the ip address of the server to connect to
        :param port: port number
        :param receive_message_queue: the queue to receive messages from (server)
        :param send_message_queue: the queue to sendn
        :param buf: the buffer size to send/receive messages (default to 1024 bytes)
        """
        self.buf = buf
        self.ip = server_ip
        self.port = port
        # try to connect to server
        self.TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPSock.connect((self.ip, self.port))

        self.send_message_queue = send_message_queue
        self.receive_message_queue = receive_message_queue

    def start_receive(self):
        """
        Create thread to receive messages from the server
        :return: none
        """
        Thread(target=lambda: self.__start_receive_from_queue__()).start()

    def start_send(self):
        """
        Create thread to send messages to the server
        :return: none
        """
        # create thread to send msg
        Thread(target=lambda: self.__start_send_to_queue__()).start()

    def __start_receive_from_queue__(self):
        """start receiving messages from server and pass them to the receive_message_queue
        :return: none
        """
        while True:
            received_message = self.TCPSock.recv(self.buf)
            print "Server sends: " + received_message
            self.receive_message_queue.put(received_message)

    def __start_send_to_queue__(self):
        """start sending messages to server and pass them to the send_message_queue. Send 'exit' to close the socket
        :return: none
        """
        while True:
            message_to_send = str(self.send_message_queue.get())
            print "Sending", message_to_send
            self.TCPSock.send(message_to_send)
