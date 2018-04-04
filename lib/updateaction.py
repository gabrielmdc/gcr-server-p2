"""
UpdateAction module
"""
import threading
import sys

from repository.repositories import Repositories


class UpdateAction(threading.Thread):
    """
    UpdateAction class
    """

    def __init__(self, db_file, gpio, name, port, inverted):
        threading.Thread.__init__(self)
        self.__db_file = db_file
        self.__gpio = gpio
        self.__name = name
        self.__port = port
        self.__inverted = inverted

    def run(self):
        self._update_action()

    def _update_action(self):
        if not self.__gpio:
            return
        try:
            repositories = Repositories(self.__db_file)
            gpio_repo = repositories.get_gpio_repository()
            gpio_repo.update_gpio(self.__gpio.get_id(), self.__name, self.__port, self.__inverted)
            self.__gpio.set_name(self.__name)
            self.__gpio.set_port(self.__port)
            self.__gpio.set_inverted(self.__inverted)
        except Exception as e:
            sys.stderr.write(e.message)
