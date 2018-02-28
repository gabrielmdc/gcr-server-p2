"""
Connection module
"""
import socket
import threading
from receiver import ReceiverThread
from sender import SenderThread
from supervisor import SupervisorThread


class Connection(threading.Thread):
    """
    Connection class
    """

    def __init__(self, connection, address_port, event, db_file):
        """
        Constructor
        :param connection: socket connection
        :param address_port: integer
        :param event: Threading.Event
        :param db_file: string
        """
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__address_port = address_port
        self.__event = event
        self.__db_file = db_file

    def run(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.connect(self.__address_port)
        gpios = SupervisorThread.gpios
        init_message = SenderThread.get_gpios_json(gpios)
        sender = SenderThread(self.__event, sender_socket, init_message)
        receiver = ReceiverThread(self.__connection, self.__db_file, sender)
        receiver.start()
        sender.start()
