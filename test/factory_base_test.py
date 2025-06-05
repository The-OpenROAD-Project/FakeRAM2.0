#!/usr/bin/env python3

import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from factory_base import FactoryBase


class DPRAM:
    """Test class for DPRAM"""

    def __init__(self, name, width_in_bits, depth, num_banks, process, timing_data):
        pass

    def get_type(self):
        return "DPRAM"


class SPRAM:
    """Test class for SPRAM"""

    def __init__(self, name, width_in_bits, depth, num_banks, process, timing_data):
        pass

    def get_type(self):
        return "SPRAM"


class FactoryBaseTest(unittest.TestCase):
    """Unit test for FactoryBase class"""

    def setUp(self):
        """Sets up factory by registering two types of SRAMs"""
        FactoryBase.register("RAM", "DP", DPRAM)
        FactoryBase.register("RAM", "SP", SPRAM)

    def test_basic(self):
        """Tests calling factory with existent and non existent keys"""
        width = 32
        depth = 256
        banks = 2
        dpram = FactoryBase.create(
            "dpram", width, depth, banks, "RAM", "DP", None, None
        )
        self.assertIsNotNone(dpram)
        self.assertEqual(dpram.get_type(), "DPRAM")
        spram = FactoryBase.create(
            "spram", width, depth, banks, "RAM", "SP", None, None
        )
        self.assertIsNotNone(spram)
        self.assertEqual(spram.get_type(), "SPRAM")
        # SP RF is not registered, so raise exception
        with self.assertRaises(Exception):
            sprf = FactoryBase.create(
                "sprf", width, depth, banks, "RF", "SP", None, None
            )


if __name__ == "__main__":
    unittest.main()
