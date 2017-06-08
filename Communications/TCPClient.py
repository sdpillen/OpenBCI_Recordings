"""
This method is for sending messages between computers on the same network.

Messages are sent as strings.  If sending a nonstring object, it will be converted
to a string.
"""
import os
import socket
import threading
import Queue
import warnings


class TCPClient(object):

    def __init__(self, server_ip, port, send_message_queue, buf=1024):
        self.buf = buf
        self.ip = server_ip
        self.port = port
        self.send_message_queue = send_message_queue
        # try to connect to server
        self.TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPSock.connect((self.ip, self.port))


    def send_to_client(self):
        """
        Reads messages from the send_messages_queue passed during initialization

        Sends data in accordance with the host and port set during initialization

        Pass 'exit' to close the socket.

        Data put on queue will be cast to a string!
        """
        while True:
            message = str(self.send_message_queue.get())
            self.TCPSock.send(message)
            back_msg = self.TCPSock.recv(self.buf)
            print "Server sends back: " + back_msg
















