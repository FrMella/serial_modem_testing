import sys, os
from serial import Serial
import configparser

configuration_modem = configparser.ConfigParser()
configuration_modem.read('modem_config.cfg')


#a = configuration_modem.get('ME910C1', 'port')

serial_config = dict(configuration_modem.items('ME910C1'))
print(serial_config)
ser = Serial.apply_settings(serial_config)
