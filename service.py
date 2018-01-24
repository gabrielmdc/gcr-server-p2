"""
Main program
"""
import sys
from main import Main

SOCKET_PORT = 10000
DB_FILE = "resources/database.db"


def main(m):
    """
    Main program
    """
    while True:
        m.listen_new_connection()


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
