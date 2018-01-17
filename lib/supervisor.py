"""
Module Supervisor
"""
import threading
from sender import SenderThread


class SupervisorThread(threading.Thread):
    """
    SupervisorThread class
    This supervises any changes for all the gpios and send them in case of changes
    """
    def __init__(self, gpios, event):
        threading.Thread.__init__(self)
        self.__event = event
        self.__gpios = gpios

    def __get_changed_ports(self):
        """
        Get a list of ports whose port status has changed
        """
        changed_gpios = []
        for gpio in self.__gpios:
            if gpio.has_changed():
                changed_gpios.append(gpio)
                gpio.changes_send()
        return changed_gpios

    def run(self):
        while True:
            try:
                ports_to_send = self.__get_changed_ports()
                if len(ports_to_send) > 0:
                    msg = SenderThread.get_gpios_json(ports_to_send)
                    SenderThread.msg = msg
                    self.__event.set()
                    self.__event.clear()
            except Exception as e:
                print(e)
                self.__event.set()
                self.__event.clear()
                break
