"""
AddAction module
"""
import threading
import sys
import os

from models.gpio import Gpio
from repository.repositories import Repositories
from supervisor import SupervisorThread


class AddAction(threading.Thread):
    """
    Add class
    """

    def __init__(self, db_file, name, port, inverted):
        threading.Thread.__init__(self)
        self.__db_file = db_file
        self.__name = name
        self.__port = port
        self.__inverted = inverted

    def run(self):
        self._add_action()

    def _add_action(self):
        try:
            repositories = Repositories(self.__db_file)
            gpio_repo = repositories.get_gpio_repository()
            new_gpio = gpio_repo.create_gpio(self.__name, self.__port, self.__inverted)
            AddAction.prepare_gpios([new_gpio])
            SupervisorThread.gpios.append(new_gpio)
        except Exception as e:
            sys.stderr.write(e.message)

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
            gpio_status = '1' if gpio.is_inverted() else '0'
            script = "sh " + script_path + " " + str(gpio.get_port()) + " " + gpio_status
            try:
                os.system(script)
            except Exception as e:
                sys.stderr.write('On Gpio: ' + str(gpio.get_port()) + e.message)
