"""
Main program
"""
import os
import socket
import threading
from lib.connection import Connection
from lib.receiver import ReceiverThread
from lib.supervisor import SupervisorThread
from lib.repository.repositories import Repositories


class Main(object):
    """
    Main class
    """
    def __init__(self, socket_port, db_file):
        self.__socket_port = socket_port
        self.__event = threading.Event()
        self.__db_file = db_file
        self.__socket = None
        self.__prepare_socket()
        self.__supervisor = None

        repositories = Repositories(self.__db_file)
        gpio_repository = repositories.get_gpio_repository()
        gpios = gpio_repository.get_all_gpio()
        ReceiverThread.gpios = gpios
        # self.__supervisor = SupervisorThread(gpios, self.__event)
        Main.prepare_gpios(gpios)
        # self.__supervisor.start()

    def listen_new_connection(self):
        # Wait for a connection
        conn, client_address = self.__socket.accept()
        connection = Connection(conn, (client_address[0], self.__socket_port), self.__event, self.__db_file)
        connection.start()

        if not self.__supervisor:
            gpios = ReceiverThread.gpios
            self.__supervisor = SupervisorThread(gpios, self.__event)
            self.__supervisor.start()

    def close_socket_connection(self):
        print('Closing connections and threads...')
        self.__socket.close()
        self.__supervisor.stop()

    def __prepare_socket(self):
        if not self.__socket:
            # Create a TCP/IP socket
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = ('', self.__socket_port)
        self.__socket.bind(server_address)
        # Listen for incoming connections
        self.__socket.listen(1)

    @staticmethod
    def prepare_gpios(gpios):
        """
        Prepare the gpio port to be used
        """
        for gpio in gpios:
            service_path = os.path.dirname(os.path.realpath(__file__))
            script_path = os.path.join(service_path, 'lib', 'gpio_setup.sh')
            try:
                os.system("sh " + script_path + " " + str(gpio.get_port()))
            except Exception:
                print('On GPIO: ' + str(gpio.get_port()))
                print(Exception.message)
