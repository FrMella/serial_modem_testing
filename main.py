from modem2 import Modem
from serial import Serial
import time, sys
import datetime




com = 'AT\n'

Modem.send_command(com)
