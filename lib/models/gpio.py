"""
Gpio module
"""
import os


class Gpio(object):
    """
    Gpio class
    """
    STATUS_ON = '1'
    STATUS_OFF = '0'
    STATUS_UNKNOWN = ''

    def __init__(self, gpio_id, name, port, gpio_directory_name):
        self.file_name = Gpio.get_file_name(gpio_directory_name, port)
        self.__id = gpio_id
        self.__name = name
        self.__port = port
        self.__status = Gpio.STATUS_UNKNOWN
        self.__has_changed = True

    def changes_send(self):
        """
        Set __has_changed = False
        This represents that the gpio changes has been send
        :return: void
        """
        self.__has_changed = False

    def has_changed(self):
        self.__check_status()
        return self.__has_changed

    def set_name(self, name):
        if self.__name != name:
            self.__name = name
            self.__has_changed = True

    def set_port(self, port):
        if self.__port != port:
            self.__port = port
            self.__has_changed = True

    def set_status(self, status):
        if self.__status != status:
            self.__status = status
            self.__write_status()
            self.__has_changed = True

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_port(self):
        return self.__port

    def get_status(self):
        return self.__status

    @staticmethod
    def get_file_name(parent_dir_name, port):
        return os.path.join(parent_dir_name, "gpio" + str(port), 'value')

    def __read_status(self):
        """
        Return status from the file and set the new status
        """
        with open(self.file_name) as f:
            return f.read(1)

    def __write_status(self):
        """
        Write the status in the file
        """
        with open(self.file_name, "w") as f:
            f.write(self.__status)

    def __check_status(self):
        if self.__status_has_changed():
            self.__has_changed = True

    def __status_has_changed(self):
        """
        Return True if the status has changed from the file, otherwise return False
        """
        status_from_file = self.__read_status()
        if status_from_file != '' and self.__status != status_from_file:
            self.__status = status_from_file
            return True
        return False
