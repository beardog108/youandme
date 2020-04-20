import sys

import stem

OWN_TOR = False
try:
    from .starttor import launch_tor
    OWN_TOR = True
except ModuleNotFoundError:
    pass

