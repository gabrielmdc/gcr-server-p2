"""
Receiver module
Protocol:
------------------
END
STATUS:id_gpio,...:'ON' | 'OFF'
GET:ALL | id_gpio
EDIT:id_gpio:name:port
ADD:name:port
DELETE:id_gpio
------------------
"""
import threading
from sender import SenderThread
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/models")
from gpio import Gpio


class ReceiverThread(threading.Thread):
    """
    ReceiverThread class
    """
    gpios = []

    def __init__(self, connection, repositories):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__repositories = repositories

    def run(self):
        while True:
            # Receive the data in small chunks and retransmit it
            msg = self.__connection.recv(100)
            # Protocol: MSG:INFO|ON|OFF
            action_data = ReceiverThread.get_action_data(msg)
            if not action_data:
                continue
            action = action_data[0]
            data = action_data[1]

            if action == 'END' or not data:
                self.__connection.close()
                break

            if action == 'STATUS':
                if data[1] == 'ON':
                    status = Gpio.STATUS_ON
                elif data[1] == 'OFF':
                    status = Gpio.STATUS_OFF
                else:
                    continue
                # Get gpios
                gpios = ReceiverThread.get_gpios_from_data(data[0])
                # modify the status of all gpios
                for gpio in gpios:
                    gpio.set_status(status)

            elif action == 'GET':
                if not data:
                    continue
                if data[0] == 'ALL':
                    msg_to_send = SenderThread.get_gpios_json(ReceiverThread.gpios)
                    self.__connection.sendall(msg_to_send.encode())
                else:
                    gpio = ReceiverThread.get_gpio_by_id(data[0])
                    msg_to_send = SenderThread.get_gpios_json([gpio])
                    self.__connection.sendall(msg_to_send.encode())

            elif action == 'EDIT' and len(data) > 2:
                gpio = ReceiverThread.get_gpio_by_id(data[0])
                if not gpio:
                    continue
                gpio.set_name(data[1])
                gpio.set_port(data[2])
                gpio_repo = self.__repositories.get_gpio_repository()
                gpio_repo.update_gpio(gpio)

            elif action == 'ADD' and len(data) > 1:
                gpio_repo = self.__repositories.get_gpio_repository()
                new_gpio = gpio_repo.create_gpio(data[0], data[1])
                new_gpio.set_status(Gpio.STATUS_OFF)
                ReceiverThread.gpios.append(new_gpio)
            elif action == 'DELETE' and len(data) > 0:
                gpio = ReceiverThread.get_gpio_by_id(data[0])
                if not gpio:
                    continue
                gpio_repo = self.__repositories.get_gpio_repository()
                gpio_repo.delete_gpio(gpio)

    @staticmethod
    def get_gpio_by_id(gpio_id):
        for gpio in ReceiverThread.gpios:
            if gpio.id == gpio_id:
                return gpio
        return None

    @staticmethod
    def get_gpios_from_data(data):
        if data:
            gpios_id = data.split(',')
            id_list = list(filter(None, gpios_id))
            gpios = ReceiverThread.get_gpios_from_id_list(id_list)
            return gpios
        return []

    @staticmethod
    def get_gpios_from_id_list(id_list):
        gpios = []
        for gpio in ReceiverThread.gpios:
            if gpio.id in id_list:
                gpios.append(gpio)
        return gpios

    @staticmethod
    def get_action_data(msg):
        data_action = msg.split(':')
        if len(data_action) > 0:
            action = data_action[0]
            data = data_action[1:]
            return action, data
        return None
