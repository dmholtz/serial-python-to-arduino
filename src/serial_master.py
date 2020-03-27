"""Implements a master - client concept for serial communication between a
computer and a embedded device such as a Arduino board.

by dmholtz

"""

import serial
import serial.tools.list_ports_windows
import serial.tools.list_ports_linux
import time
import sys
import platform

class SerialCommunicator():

    SETUP_INIT = 0xFF

    def __init__(self, port, baudrate = 115200):
        """Initializes a SerialCommunicator object by trying to establish a 
        serial connection.

        Args:
            * port (String): name of the port, e.g. 'COM4'

        Raises:
            * IOError: if the desired connection cannot be established

        """

        try:
            print('Trying to connect to port', port, end='')
            self.port = serial.Serial(port, baudrate)       
            
            # Wait 3 seconds, otherwise serial communication might fail
            for i in range(100):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(0.03)
            print('\nSuccessfully connect to port', port,'@baudrate:', baudrate)
        except:
            raise IOError('Cannot connect to port '+port)


    @classmethod
    def autoconnect(cls, baudrate = 115200):
        """Gathers all the available ports and automatically connects to the
        first port in the list.

        Raises:
            * IOError: if no COM device is available

        """

        available_ports = SerialCommunicator.list_ports(log_enabled=False)

        if len(available_ports) < 1:
            raise IOError('No Serial devices available, cannot connect.')

        autoport = available_ports[0]
        return cls(autoport, baudrate)

    @staticmethod
    def list_ports(log_enabled = True):
        """Determines the platform and returns a list of all available port
        names. Console logging is optional.
        
        """

        plt = platform.system() # determine platform
        platform_switcher = {
            'Windows': serial.tools.list_ports_windows,
            'Linux': serial.tools.list_ports_linux
        }

        available_ports = platform_switcher.get(plt).comports()
        if log_enabled:
            print('Available devices:', len(available_ports))
        port_identifiers = list()
        for port in available_ports:
            if log_enabled:
                print('-',port)
            port_identifiers.append(port.device)

        return port_identifiers

    def client_setup(self, int_rep, msg_length, batch_size):

        self.int_rep = int_rep
        self.msg_length = msg_length
        self.batch_size = batch_size

    @staticmethod
    def to_bytes(value, size = 1):
        """Splits an integer value into bytes and returns them as a list.

        Args:
            * size (int): must be positive integer > 0
            * value (int): must be a integer within the range of 'size' bytes.

        """

        if type(value) is not int:
            raise ValueError('Information loss - value is not int')
        if not size >= 1 or type(size) is not int:
            raise ValueError('size must be a positive integer')
        upper_bound = 2**(8*size-1)
        if not value < upper_bound or not value >= -upper_bound:
            raise ValueError('Information loss - value exceeds boundaries')

        result = list()
        if value >= 0:
            for i in range(size):
                result.append(value % 256)
                value = value // 256
            result.reverse()
        else:
            result = SerialCommunicator.to_bytes(value+upper_bound, size)
            result[0] = result[0]+128 # set the sign bit (-1) by adding 128

        return result

    @staticmethod
    def to_bytestream(values, size = 1):
        """Returns a list of values into a bytestream by passing each value
        through to_bytes() and concatenating the result.

        Args:
            * size (int): size of each value in values, requires size > 0
            * values (list): list of integers

        """
        
        result = list()
        for value in values:
            result.extend(SerialCommunicator.to_bytes(value, size))
        return result



        
        
        