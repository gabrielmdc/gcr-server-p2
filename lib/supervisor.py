"""
Module Supervisor
"""
import threading
import sys
from sender import SenderThread


class SupervisorThread(threading.Thread):
    """
    SupervisorThread class
    This supervises any changes for all the gpios and send them in case of changes
    """
    gpios = []

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.__event = event
        self.__nonStop = True

    @staticmethod
    def get_changed_ports():
        """
        Get a list of ports whose port status has changed
        :return: Gpio[]
        """
        changed_gpios = []
        for gpio in SupervisorThread.gpios:
            if gpio.to_delete:
                SupervisorThread.gpios.remove(gpio)
                changed_gpios.append(gpio)
                continue
            if gpio.has_changed():
                changed_gpios.append(gpio)
                gpio.changes_send()
        return changed_gpios

    def run(self):
        while self.__nonStop:
            try:
                ports_to_send = SupervisorThread.get_changed_ports()
                if len(ports_to_send) > 0:
                    msg = SenderThread.get_gpios_json(ports_to_send)
                    SenderThread.msg = msg
                    SupervisorThread.deleted_gpios = []
                    self.__event.set()
                    self.__event.clear()
            except Exception as e:
                sys.stderr.write(e.message)
                break

    def stop(self):
        """
        Set a field to indicate that the thread must be stopped
        :return: void
        """
        self.__nonStop = False