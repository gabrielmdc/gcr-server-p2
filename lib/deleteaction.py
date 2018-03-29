"""
DeleteAction module
"""
import threading
import sys
from repository.repositories import Repositories


class DeleteAction(threading.Thread):
    """
    DeleteAction class
    """

    def __init__(self, db_file, gpio):
        threading.Thread.__init__(self)
        self.__db_file = db_file
        self.__gpio = gpio

    def run(self):
        self._delete_action()

    def _delete_action(self):
        if not self.__gpio:
            return
        try:
            repositories = Repositories(self.__db_file)
            gpio_repo = repositories.get_gpio_repository()
            gpio_repo.delete_gpio_by_id(self.__gpio.get_id())
            self.__gpio.to_delete = True
        except Exception as e:
            sys.stderr.write(e.message)
