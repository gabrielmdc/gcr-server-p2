"""
Main program
"""
import sys
from main import Main

SOCKET_PORT = 10001
DB_FILE = "lib/resources/database.db"


def main(m):
    """
    Main program
    """
    i = 5
    while i > 0:
        i -= 1
        try:
            m.listen_new_connection()
        except TypeError:
            print('exception?')
            break


if __name__ == '__main__':
    m = Main(SOCKET_PORT, DB_FILE)
    try:
        main(m)
    except (KeyboardInterrupt, SystemExit):
        print('Bye!')
    finally:
        m.close_socket_connection()
        sys.exit(1)
sys.exit(1)
