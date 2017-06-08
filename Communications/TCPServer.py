import os
import socket
import Queue
import threading
import warnings

class TCPServer(object):

    def __init__(self, port, receive_message_queue, host="", buf=1024):
        """
        Sends messages to the specified host and port for computers on the same network.
        :param host: Defaults to ""
        :param port: Set to desired port. Only one Send object can be opened on a given port. Example: 13000
        :param send_message_queue: Place messages on this queue to have them sent.
        """
        self.port = port
        self.buf = buf
        self.addr = ('', self.port)
        # TCP
        self.TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPSock.bind(self.addr)
        self.TCPSock.listen(1)
        # accept the connection
        self.conn, self.client_addr = self.TCPSock.accept()
        self.receive_message_queue = receive_message_queue

    def receive_from_queue(self):
        """
        Receives messages and passes them to the receive_message_queue passed during initialization
    
        Received data in accordance with the host and port set during initialization
    
        Pass 'exit' to close the socket.
    
        All data passed is of string format -- meaning all data placed on the receive_message_queue will
        be a string.
        """
        while True:
            message = str(self.conn.recv(self.buf))
            self.receive_message_queue.put(message)
            print "received message: " + message
            if message == "exit":
                self.TCPSock.close()

    def sent_back_to_client(self):
        while True:
            self.conn.sendall(self.receive_message_queue.get())
