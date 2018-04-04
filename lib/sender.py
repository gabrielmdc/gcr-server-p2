"""
Sender module
"""
import threading
import json

import sys


class SenderThread(threading.Thread):
    """
    SenderThread class
    """
    msg = ''

    def __init__(self, event, sender_socket, init_message):
        """
        Constructor
        :param event: Threading.Event
        :param sender_socket: Socket connection
        :param init_message: string: to be send for the first time in a connection
        """
        threading.Thread.__init__(self)
        self.__sender_socket = sender_socket
        self.__event = event
        self.__init_message = init_message

    def run(self):
        if self.__sender_socket and not self._send_message(self.__init_message):
            return
        while self.__sender_socket:
            if not self._send_message(SenderThread.msg):
                break

    def close_connection(self):
        """
        Clean up the connection
        :return: void
        """
        self.__sender_socket.close()
        self.__event.set()
        self.__event.clear()

    @staticmethod
    def get_gpios_json(gpios):
        """
        Return a string in Json format with port numbers and their status
        :param gpios: Gpios[]
        :return: string
        """
        gpios_to_json = []
        for gpio in gpios:
            gpio_dict = {
                'id': gpio.get_id(),
                'name': gpio.get_name(),
                'port': gpio.get_port(),
                'inverted': 'true' if gpio.is_inverted() else 'false',
                'status': gpio.get_status(),
                'deleted': 'true' if gpio.to_delete else 'false'
            }
            gpios_to_json.append(gpio_dict)
        return json.dumps(gpios_to_json)

    def _send_message(self, message):
        """
        Return True or False, depending on: if the message was send successfully
        :param message: string
        :return: boolean
        """
        try:
            self.__sender_socket.send(message.encode())
            self.__event.wait()
        except Exception as e:
            sys.stderr.write(e.message)
            self.close_connection()
            return False
        return True
