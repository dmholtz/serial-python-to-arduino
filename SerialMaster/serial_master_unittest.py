from serial_master import SerialCommunicator

import unittest
from test import support
import time
import random

class SerialCommunicatorTest(unittest.TestCase):
    """Tests the Serial Communicator and its methods.

    """
    def setUp(self):
        random.seed(1)
        pass

    def test_to_byte(self):
        # positive integers and 0 within boundary
        result = SerialCommunicator.to_bytes(256,2)
        assert result == list([1,0])
        result = SerialCommunicator.to_bytes(0,6)
        assert result == list([0]*6)
        result = SerialCommunicator.to_bytes(1234,2)
        assert result == list([4,210])
        # negative integers within boundary
        result = SerialCommunicator.to_bytes(-128,1)
        assert result == list([128])
        result = SerialCommunicator.to_bytes(-1,2)
        assert result == list([255,255])
        result = SerialCommunicator.to_bytes(-32768,2)
        assert result == list([128,0])
        # exceptions
        self.assertRaises(ValueError, SerialCommunicator.to_bytes, 0,0)
        self.assertRaises(ValueError, SerialCommunicator.to_bytes, 256,1)
        self.assertRaises(ValueError, SerialCommunicator.to_bytes, -34567,2)

    def test_to_bytestream(self):
        values = list([256, 1234, -1, -32768])
        result = SerialCommunicator.to_bytestream(values, 2)
        assert result == list([1,0,4,210,255,255,128,0])
        values = list()
        result = SerialCommunicator.to_bytestream(values, 2)
        assert result == list()
        # exceptions
        values = list([256, 1234, 32768])
        self.assertRaises(ValueError, SerialCommunicator.to_bytestream, values)

    def test_communicaton(self):
        # Config
        int_rep = 2
        msg_length = 6
        batch_size = 20
        # Hardware setup
        communicator = SerialCommunicator.autoconnect()
        communicator.client_setup(int_rep, msg_length, batch_size)
        # Send one batch
        startTime = time.time()
        communicator.send(self.create_sample_commands())
        print('Elapsed time for one batch:',time.time()-startTime)

        # start stress-testing
        num = 50
        print('Stress testing, send', num, 'random batches')
        startTime = time.time()
        cmds = self.create_random_comands(int_rep, msg_length, batch_size)
        for _ in range(num):
            communicator.send(cmds)
        print('Elapsed time for',num, 'random batches:', time.time()-startTime)

    def create_sample_commands(self):
        cmd = (55, list([12,14,14,15,16,17]))
        cmds = list()
        cmds.append(cmd)
        cmds = cmds * 20
        return cmds

    def create_random_comands(self, int_rep, msg_length, batch_size):
        max_val = 2**(8*int_rep-1)-1
        min_val = -max_val - 1
        
        cmds = list()
        for _ in range(batch_size):
            operation = random.randrange(1,254)
            params = random.sample(range(min_val, max_val), msg_length)
            cmd = (operation, params)
            cmds.append(cmd)
        print(cmds)
        return cmds
