import sys

try:
    from youandme.tor import launch_tor
except ModuleNotFoundError:
    pass

from youandme.server import server

def interactive_connector():

    print("Starting Tor...")
    launch_tor()
    print("Tor started.")
    server()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'interactive':
            interactive_connector()
