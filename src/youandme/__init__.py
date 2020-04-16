import sys

try:
    from .starttor import launch_tor
except ModuleNotFoundError:
    pass

from .server import server

def interactive_connector():
    server()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'interactive':
            interactive_connector()
