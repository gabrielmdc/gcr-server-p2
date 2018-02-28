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

    def __init__(self, event, connection, init_message):
        """
        Constructor
        :param event: Threading.Event
        :param connection: Socket connection
        :param init_message: string: to be send for the first time in a connection
        """
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__event = event
        self.__init_message = init_message

    def run(self):
        if self.__connection and not self._send_message(self.__init_message):
            return
        while self.__connection:
            if not self._send_message(SenderThread.msg):
                break

    def close_connection(self):
        """
        Clean up the connection
        :return: void
        """
        self.__connection.close()
        self.__connection = None
        self.__event.set()
        self.__event.clear()
        #print('Sender disconnected')

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
            #print('sending message: ' + message)
            self.__connection.sendall(message.encode())
            self.__event.wait()
        except Exception as e:
            sys.stderr.write(e.message)
            self.close_connection()
            return False
        return True
