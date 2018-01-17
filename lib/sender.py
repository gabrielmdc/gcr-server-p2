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

    def __init__(self, event, connection):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__event = event

    def run(self):
        while True:
            try:
                self.__connection.sendall(SenderThread.msg.encode())
                self.__event.wait()
            except Exception as e:
                print(e)
                # Clean up the connection
                self.__connection.close()
                break

    @staticmethod
    def get_gpios_json(gpios):
        """
        Return a string in Json format with port numbers and their status
        """
        return json.dumps([gpio.__dict__ for gpio in gpios])
