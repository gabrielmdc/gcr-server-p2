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
        """
        Constructor
        :param db_file: string
        """
        self.__con = sqlite3.connect(db_file)
        self.__gpio_repository = None

    def get_gpio_repository(self):
        """
        Get gpio repository
        :return: GpioRepository
        """
        if self.__con and not self.__gpio_repository:
            self.__gpio_repository = GpioRepository(self.__con)
            self.__gpio_repository.create_table()
        return self.__gpio_repository
