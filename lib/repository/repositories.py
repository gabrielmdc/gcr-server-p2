"""
Repositories module
"""
import sqlite3
from gpio import GpioRepository


class Repositories(object):
    """
    Repositories class
    """
    def __init__(self, db_file):
        self.__con = sqlite3.connect(db_file)
        self.__gpio_repository = None

    def get_gpio_repository(self):
        """
        Get gpio repository
        :return:
        """
        if self.__con and not self.__gpio_repository:
            self.__gpio_repository = GpioRepository(self.__con)
        return self.__gpio_repository
