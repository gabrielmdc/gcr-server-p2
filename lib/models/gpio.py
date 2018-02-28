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

    def __init__(self, gpio_id, name, port, inverted, gpio_directory_name):
        """

        :param gpio_id: integer
        :param name: string
        :param port: integer
        :param inverted: boolean
        :param gpio_directory_name: string
        """
        self.file_name = Gpio.get_file_name(gpio_directory_name, port)
        self.__id = gpio_id
        self.__name = name
        self.__port = port
        self.__status = Gpio.STATUS_UNKNOWN
        self.__has_changed = False
        self.__inverted = inverted
        self.to_delete = False

    def changes_send(self):
        """
        Set __has_changed = False
        This represents that the gpio changes has been send
        :return: void
        """
        self.__has_changed = False

    def has_changed(self):
        """
        Check if the status has been changed in the file (on, off) and
        return True if the status or any other field has been changed
        :return: boolean
        """
        self.refresh_status()
        return self.__has_changed

    def refresh_status(self):
        """
        Refresh the status and set '__has_changed' = True, if the status has changed from the file
        :return: void
        """
        status_from_file = self.__read_status()
        if status_from_file != '' and self.__status != status_from_file:
            prev_status = self.__status
            self.__status = status_from_file
            self.__has_changed = True

    def set_name(self, name):
        """
        Set the name
        Set 'has changed' = true
        :param name: string
        :return: void
        """
        if self.__name != name:
            self.__name = name
            self.__has_changed = True

    def set_port(self, port):
        """
        Set the port
        Set 'has changed' = true
        :param port: integer
        :return: void
        """
        if self.__port != port:
            self.__port = port
            self.__has_changed = True

    def set_status(self, status):
        """
        Set the status
        Set 'has changed' = true
        :param status: string
        :return: void
        """
        if self.__status != status:
            self.__write_status(status)

    def set_inverted(self, inverted):
        """
        Set the inverted field
        Set 'has changed' = true
        :param inverted: boolean
        :return: void
        """
        if self.__inverted != inverted:
            self.__inverted = inverted
            self.__has_changed = True

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_port(self):
        return self.__port

    def get_status(self):
        return self.__status

    def is_inverted(self):
        return self.__inverted

    @staticmethod
    def get_file_name(parent_dir_name, port):
        return os.path.join(parent_dir_name, "gpio" + str(port), 'value')

    def __read_status(self):
        """
        Return status from the file and set the new status
        :return: string
        """
        with open(self.file_name) as f:
            status = f.read(1)
            if self.__inverted:
                status = Gpio.STATUS_ON if status == Gpio.STATUS_OFF else Gpio.STATUS_OFF
            return status

    def __write_status(self, status):
        """
        Write the status in the file
        :param status: boolean
        :return: void
        """
        if status != Gpio.STATUS_OFF and status != Gpio.STATUS_ON:
            return
        if self.__inverted:
            status = Gpio.STATUS_ON if status == Gpio.STATUS_OFF else Gpio.STATUS_OFF
        with open(self.file_name, "w") as f:
            f.write(status)
