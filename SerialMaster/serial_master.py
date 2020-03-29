"""Implements a master - client concept for serial communication between a
computer and a embedded device such as a Arduino board.

by dmholtz

"""

import serial
import serial.tools.list_ports_windows
import serial.tools.list_ports_linux
from itertools import zip_longest
import time
import sys
import platform

class SerialCommunicator():

    SETUP_INIT_BYTE = 0xFF

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
            for i in range(50):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(0.06)
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

    def client_setup(self, int_rep, msg_length, batch_size):

        self.int_rep = 1
        self.msg_length = 3
        self.batch_size = 1
        self.bytes_per_cmd = 4

        setup_params = list([int_rep, msg_length, batch_size])
        setup_params = SerialCommunicator.to_bytestream(setup_params, size=1)
        setup_cmd = list([(SerialCommunicator.SETUP_INIT_BYTE, setup_params)])
        print(setup_cmd)
        self.send(setup_cmd)

        self.int_rep = int_rep
        self.msg_length = msg_length
        self.bytes_per_cmd = msg_length * self.int_rep + 1
        self.batch_size = batch_size

    def send(self, commands):
        """Converts a list of command tuples into a list of byte commands, i.e.
        a list of a list of bytes. Sends the byte commands as a batch.

        Args:
            * commands (list(): list of command tuples (operation_id, params), 
            list must contain between one and 'self.batch_size' tuples.

        """

        if len(commands) > self.batch_size or len(commands) < 1:
            raise ValueError('Number of commands must be at least one and may \
                not exceed the batch size.')

        byte_cmds = list()
        for (operation_id, params) in commands:
            byte_cmd = list()
            byte_cmd.append(operation_id)
            byte_cmd.extend(SerialCommunicator.to_bytestream(params, \
                 size = self.int_rep))
            byte_cmds.append(byte_cmd)

        self._send_batch(byte_cmds)

    def _send_batch(self, byte_cmds):
        """Sends a list of bytes and awaits the clients responds

        """
        assert self.batch_size >= len(byte_cmds)
        for (_, cmd) in zip_longest(range(self.batch_size), byte_cmds, \
            fillvalue=self._empty_cmd()):
            self.port.write(bytes(cmd))
        while self.port.in_waiting < 1:
            pass
        print(self.port.readline())

    def _empty_cmd(self):
        """Returns an empty command consisting only of zero bytes and this
        instance's messeage length.
        """

        return [0]*self.bytes_per_cmd

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
            for _ in range(size):
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

    



        
        
        