"""
This method is for sending messages between computers on the same network.

Messages are sent as strings.  If sending a nonstring object, it will be converted
to a string.
"""
import os
import socket
import threading
import Queue


class TCPClient(object):

    def __init__(self, server_ip, port, receive_message_queue, send_message_queue, buf=1024):
        self.buf = buf
        self.ip = server_ip
        self.port = port
        # try to connect to server
        self.TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPSock.connect((self.ip, self.port))

        self.send_message_queue = send_message_queue
        self.receive_message_queue = receive_message_queue

    def start_receive_from_queue(self):
        while True:
            received_message = self.TCPSock.recv(self.buf)
            print "Server sends: " + received_message
            self.receive_message_queue.put(received_message)

    def start_send_to_queue(self):
        """
        Reads messages from the send_messages_queue passed during initialization

        Sends data in accordance with the host and port set during initialization

        Pass 'exit' to close the socket.

        Data put on queue will be cast to a string!
        """
        while True:
            message_to_send = str(self.send_message_queue.get())
            print "Sending", message_to_send
            self.TCPSock.send(message_to_send)



















