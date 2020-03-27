from serial_master import SerialCommunicator

import unittest
from test import support

class SerialCommunicatorTest(unittest.TestCase):
    """Tests the Serial Communicator and its methods.

    """
    def setUp(self):
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
