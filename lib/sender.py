"""
Sender module
"""
import threading
import json


class SenderThread(threading.Thread):
    """
    SenderThread class
    """
    msg = ''

    def __init__(self, event, connection, init_message):
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
        #Clean up the connection
        self.__connection.close()
        self.__connection = None
        self.__event.set()
        self.__event.clear()
        print('Sender disconnected')

    def _send_message(self, message):
        """
        Return True or False, depending on: if the message was send successfully
        :param message:
        :return: boolean
        """
        try:
            print('sending message: ' + message)
            self.__connection.sendall(message.encode())
            self.__event.wait()
        except Exception as e:
            print(e)
            self.close_connection()
            return False
        return True

    @staticmethod
    def get_gpios_json(gpios, deleted = False):
        """
        Return a string in Json format with port numbers and their status
        """
        gpios_to_json = []
        for gpio in gpios:
            gpio_dict = {
                'id': gpio.get_id(),
                'name': gpio.get_name(),
                'port': gpio.get_port(),
                'status': gpio.get_status(),
                'deleted': 'true' if deleted else 'false'
            }
            gpios_to_json.append(gpio_dict)
        return json.dumps(gpios_to_json)
