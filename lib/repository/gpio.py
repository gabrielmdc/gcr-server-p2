"""
GpioRepository module
"""
from ..models.gpio import Gpio


class GpioRepository(object):
    """
    GpioRepository class
    """
    GPIO_DIRECTORY_NAME = "/sys/class/gpio"

    def __init__(self, con):
        self.con = con

    def create_table(self):
        cursor = self.con.cursor()
        cursor.execute('''CREATE TABLE if not exists GPIO(
            ID       INTEGER  PRIMARY KEY AUTOINCREMENT,
            NAME     TEXT             NOT NULL,
            PORT     INT              UNIQUE,
            INVERTED INT              DEFAULT 0
        )''')
        self.con.commit()

    def get_all_gpio(self):
        """
        Get all the Gpio
        :return: Gpio[]
        """
        cursor = self.con.cursor()
        cursor.execute("SELECT * from GPIO")
        gpios = []
        for t in cursor:
            gpio = Gpio(t[0], t[1], t[2], t[3] != 0, GpioRepository.GPIO_DIRECTORY_NAME)
            gpios.append(gpio)
        return gpios

    def create_gpio(self, name, port, inverted):
        is_inverted = '1' if inverted else '0'
        cursor = self.con.cursor()
        cursor.execute("INSERT INTO GPIO (NAME, PORT, INVERTED)\
          VALUES ('" + name + "', " + str(port) + ", " + is_inverted + ")")
        self.con.commit()
        return self.get_gpio_by_port(port)

    def get_gpio_by_id(self, gpio_id):
        cursor = self.con.cursor()
        cursor.execute("SELECT * from GPIO WHERE ID=" + str(gpio_id) + "")
        t = cursor.fetchone()
        gpio = Gpio(t[0], t[1], t[2], GpioRepository.GPIO_DIRECTORY_NAME)
        return gpio

    def get_gpio_by_port(self, port):
        cursor = self.con.cursor()
        cursor.execute("SELECT * from GPIO WHERE PORT=" + str(port) + "")
        t = cursor.fetchone()
        if t:
            gpio = Gpio(t[0], t[1], t[2], t[3] != 0, GpioRepository.GPIO_DIRECTORY_NAME)
            return gpio
        return None

    def delete_gpio_by_id(self, gpio_id):
        cursor = self.con.cursor()
        cursor.execute("DELETE from GPIO WHERE ID=" + str(gpio_id) + "")
        self.con.commit()

    def update_gpio(self, gpio_id, name, port, inverted):
        is_inverted = '1' if inverted else '0'
        cursor = self.con.cursor()
        cursor.execute("UPDATE GPIO set NAME='" + name + "',\
         PORT=" + str(port) + ", INVERTED=" + is_inverted + " WHERE ID=" + str(gpio_id) + "")
        self.con.commit()
