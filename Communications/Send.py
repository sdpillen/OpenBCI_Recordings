"""
This method is for sending messages between computers on the same network.

Messages are sent as strings.  If sending a nonstring object, it will be converted
to a string.
"""
import os
import socket

class Send(object):

    def __init__(self, host, port, send_message_queue):
        """
        Sends messages to the specified host and port for computers on the same network.
        
        :param host: Set to the ip address of the target computer (example: 173.250.XXX.XX)
        :param port: Set to desired port. Only one Send object can be opened on a given port. Example: 13000
        :param send_message_queue: Place messages on this queue to have them sent.
        """
        self.addr = (host, port)
        self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_message_queue = send_message_queue

    def run_send_from_queue(self):
        """
        Reads messages from the send_messages_queue passed during initialization

        Sends data in accordance with the host and port set during initialization
        
        Pass 'exit' to close the socket.
        
        Data put on queue will be cast to a string!
        """
        message = str(self.send_message_queue.get())
        self.UDPSock.sendto(message, self.addr)
        if message.lower() == "exit":
            self.UDPSock.close()
