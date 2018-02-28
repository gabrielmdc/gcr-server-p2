"""
Receiver module
Protocol:
------------------
:END
:STATUS:id_gpio,...:'ON' | 'OFF'
:EDIT:id_gpio:name:port:inverted
:ADD:name:port
:DELETE:id_gpio
------------------
"""
import threading
import os
import sys
from supervisor import SupervisorThread
from models.gpio import Gpio
from repository.repositories import Repositories


class ReceiverThread(threading.Thread):
    """
    ReceiverThread class
    """

    def __init__(self, connection, db_file, sender):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__db_file = db_file
        self.__sender = sender

    def run(self):
        while True:
            # Receive the data in small chunks and retransmit it
            msg = self.__connection.recv(32)
            msg = msg.decode('utf')
            msg = msg.strip()
            action_data = ReceiverThread.get_action_data(msg)
            #print('data received: ' + msg)
            if not action_data:
                #print('...no action_data received...')
                break
            action = action_data[0]
            data = action_data[1]
            #print('ACTION: ' + action)

            if action == 'END' or not data:
                break

            if action == 'STATUS':
                if not self._status_action(data):
                    continue

            elif action == 'EDIT':
                if not self._edit_action(data):
                    continue

            elif action == 'ADD':
                if not self._add_action(data):
                    continue

            elif action == 'DELETE':
                if not self._delete_action(data):
                    continue
        self._end()

    @staticmethod
    def get_gpio_by_id(gpio_id):
        """
        Get a Gpio by id
        :param gpio_id: integer
        :return: Gpio | None
        """
        for gpio in SupervisorThread.gpios:
            str_id = str(gpio.get_id())
            if str_id == gpio_id:
                return gpio
        return None

    @staticmethod
    def get_gpios_from_data(data):
        """
        Get gpios from the data received
        :param data: string
        :return: Gpio[]
        """
        if data:
            gpios_id = data.split(',')
            id_list = list(filter(None, gpios_id))
            gpios = ReceiverThread.get_gpios_from_id_list(id_list)
            return gpios
        return []

    @staticmethod
    def get_gpios_from_id_list(id_list):
        """
        Return Gpio[] from a list of Gpio id
        :param id_list: string[]
        :return: Gpio[]
        """
        gpios = []
        for gpio in SupervisorThread.gpios:
            str_id = str(gpio.get_id())
            if str_id in id_list:
                gpios.append(gpio)
        return gpios

    @staticmethod
    def get_action_data(msg):
        """
        Extract the action from the data received
        :param msg: string
        :return: string
        """
        data_action = msg.split(':')
        if len(data_action) > 1:
            action = data_action[1].strip()
            data = data_action[2:]
            return action, data
        return None

    @staticmethod
    def prepare_gpios(gpios):
        """
        Prepare the gpio port to be used
        :param gpios: Gpio[]
        :return: void
        """
        for gpio in gpios:
            service_path = os.path.dirname(os.path.realpath(__file__))
            script_path = os.path.join(service_path, 'gpio_setup.sh')
            try:
                os.system("sh " + script_path + " " + str(gpio.get_port()))
            except Exception as e:
                sys.stderr.write('On Gpio: ' + str(gpio.get_port()) + e)

    def _status_action(self, data):
        #print('data[1]: ' + data[1])
        if data[1] == 'ON':
            status = Gpio.STATUS_ON
        elif data[1] == 'OFF':
            status = Gpio.STATUS_OFF
        else:
            return False
        # Get gpios
        gpios = ReceiverThread.get_gpios_from_data(data[0])
        # modify the status of all gpios
        for gpio in gpios:
            #print('set status of gpio' + str(gpio.get_port()) + ' to ' + status)
            gpio.set_status(status)
        return True

    def _add_action(self, data):
        if len(data) < 3:
            return False
        try:
            repositories = Repositories(self.__db_file)
            gpio_repo = repositories.get_gpio_repository()
            new_gpio = gpio_repo.create_gpio(data[0], data[1], data[2] != '0')
            new_gpio.set_status(Gpio.STATUS_OFF)
            ReceiverThread.prepare_gpios([new_gpio])
            SupervisorThread.gpios.append(new_gpio)
        except Exception as e:
            sys.stderr.write(e.message)
            return False
        return True

    def _edit_action(self, data):
        if len(data) < 4:
            return False
        gpio = ReceiverThread.get_gpio_by_id(data[0])
        name = data[1]
        port = data[2]
        inverted = data[3]
        if not gpio:
            return False
        try:
            repositories = Repositories(self.__db_file)
            gpio_repo = repositories.get_gpio_repository()
            gpio_repo.update_gpio(gpio.get_id(), name, port, inverted)
            gpio.set_name(name)
            gpio.set_port(port)
            gpio.set_inverted(inverted)
        except Exception as e:
            sys.stderr.write(e.message)
            return False
        return True

    def _delete_action(self, data):
        if len(data) < 1:
            return False
        gpio = ReceiverThread.get_gpio_by_id(data[0])
        if not gpio:
            return False
        try:
            repositories = Repositories(self.__db_file)
            gpio_repo = repositories.get_gpio_repository()
            gpio_repo.delete_gpio_by_id(gpio.get_id())
            gpio.to_delete = True
        except Exception as e:
            sys.stderr.write(e.message)
            return False
        return True

    def _end(self):
        self.__connection.close()
        self.__sender.close_connection()
        #print('Receiver disconnected')
