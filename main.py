"""
Main program
"""
import os
import socket
import threading

import sys

from lib.connection import Connection
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
        SupervisorThread.gpios = gpios
        Main.prepare_gpios(gpios)

    def listen_new_connection(self):
        """
        Listen for new connections
        and create the supervisor in case that is not already created
        :return: void
        """
        conn, client_address = self.__socket.accept()  # conn variable is a Socket
        connection = Connection(conn, (client_address[0], self.__socket_port), self.__event, self.__db_file)
        connection.start()

        if not self.__supervisor:
            self.__supervisor = SupervisorThread(self.__event)
            self.__supervisor.start()

    def close_socket_connection(self):
        """
        Close the socket connection
        and stop the supervisor
        :return: void
        """
        print('Closing connections and threads...')
        self.__socket.close()
        self.__supervisor.stop()

    @staticmethod
    def prepare_gpios(gpios):
        """
        Prepare the gpio port to be used
        :param gpios: Gpio[]
        :return: void
        """
        for gpio in gpios:
            service_path = os.path.dirname(os.path.realpath(__file__))
            script_path = os.path.join(service_path, 'lib', 'gpio_setup.sh')
            gpio_status = '1' if gpio.is_inverted() else '0'
            script = "sh " + script_path + " " + str(gpio.get_port()) + " " + gpio_status
            try:
                os.system(script)
            except Exception as e:
                sys.stderr.write('On Gpio: ' + str(gpio.get_port()) + e.message)

    def __prepare_socket(self):
        """
        Prepare the socket for listening
        :return: void
        """
        if not self.__socket:
            # Create a TCP/IP socket
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = ('', self.__socket_port)
        self.__socket.bind(server_address)
        # Listen for incoming connections
        self.__socket.listen(1)
