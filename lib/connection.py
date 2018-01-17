"""
Connection module
"""
import socket
import threading
from receiver import ReceiverThread
from sender import SenderThread


class Connection(threading.Thread):
    """
    Connection class
    """
    def __init__(self, connection, address_port, event, repositories):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__address_port = address_port
        self.__event = event
        self.__repositories = repositories

    def run(self):
        receiver = ReceiverThread(self.__connection, self.__repositories)
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.connect(self.__address_port)
        sender = SenderThread(self.__event, sender_socket)

        receiver.start()
        sender.start()
