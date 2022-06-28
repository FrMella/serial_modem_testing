import unittest
import serial

PORT = 'loop://'

SERIAL_SETTINGS = {'baudrate', 'bytesize', 'parity', 'stopbits', 'xonxoff','dsrdtr', 'rtscts', 'timeout'
                   , 'write_timeout', 'inter_byte_timeout'}



class Test_SettingsDict(unittest.TestCase):
    """test settings dictionary structure"""

    def test_getsettings(self):
        """current settings dictionary"""
        ser = serial.serial_for_url(PORT, do_not_open=True)
        d = ser.get_settings()
        for setting in SERIAL_SETTINGS:
            self.assertEqual(getattr(ser, setting), d[setting])

    def test_partial_settings(self):
        """Partial settings test"""
        ser = serial.serial_for_url(PORT, do_not_open=True)
        d = ser.get_settings()
        del d['baudrate']
        del d['bytesize']
        ser.apply_settings(d)
        for setting in d:
            self.assertEqual(getattr(ser, setting), d[setting])

    def test_unknow_settings(self):
        """unknow settings test"""
        ser = serial.serial_for_url(PORT, do_not_open=True)
        d = ser.get_settings()
        d['foobar']= 'ignore me'
        ser.apply_settings(d)

    def test_init_sets_the_correct_attrs(self):
        """__init__ sets the correct attributes"""
        for setting, value in (
                ('baudrate', 115200),
                ('timeout', 7),
                ('write_timeout', 7),
                ('inter_byte_timeout', 15),
                ('stopbits', serial.STOPBITS_ONE),
                ('bytesize', serial.EIGHTBITS),
                ('parity', serial.PARITY_NONE),
                ('xonxoff', True),
                ('rtscts', True),
                ('dsrdtr', True)):
            kwargs = {'do_not_open': True, setting: value}
            ser = serial.serial_for_url(PORT, **kwargs)
            d = ser.get_settings()
            self.assertEqual(getattr(ser, setting), value)
            self.assertEqual(d[setting], value)

    if __name__ == '__name__':
        import sys
        sys.stdout.write(__doc__)
        if len(sys.argv) > 1:
            PORT = sys.argv[1]
        sys.stdout.write("testing port: {!r}\n".format(PORT))
        sys.argv[1:] = ['-v']
        unittest.main()

