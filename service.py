"""
Main program
"""
import sys
from main import Main

SOCKET_PORT = 10001
DB_FILE = "lib/resources/database.db"


def main():
    """
    Main program
    """
    m = Main(SOCKET_PORT, DB_FILE)
    while True:
        try:
            m.listen_new_connection()
        except TypeError:
            print('exception?')
            break
    m.close_socket_connection()


if __name__ == '__main__':
    main()
sys.exit(1)
