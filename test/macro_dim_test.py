#!/usr/bin/env python3

import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from class_process import Process
from test_utils import TestUtils
import area


class MacroDimTest(unittest.TestCase):
    """Unit test for get_macro_dimensions method"""

    def setUp(self):
        """Sets up process object used by test methods"""

        self._process = Process(TestUtils.get_base_process_data())
        # delta for use when comparing floats
        self._delta = 0.01

    def test_macro_dim(self):
        """
        Tests basic macro dimension calculation based on three bank
        configurations
        """

        banks = [1, 2, 4]
        base_height = 663.552
        base_width = 5.054
        for num_banks in banks:
            sram_data = {
                "width": 39,
                "depth": 2048,
                "banks": num_banks,
            }
            (height, width) = area.get_macro_dimensions(self._process, sram_data)
            exp_height = base_height / num_banks
            exp_width = base_width * num_banks
            self.assertAlmostEqual(height, exp_height, delta=self._delta)
            self.assertAlmostEqual(width, exp_width, delta=self._delta)

    def test_macro_dim_invalid_banks(self):
        """Tests detection that an invalid bank value was given"""

        sram_data = {
            "width": 39,
            "depth": 2048,
            "banks": 8,
        }
        with self.assertRaises(Exception):
            (height, width) = area.get_macro_dimensions(self._process, sram_data)


if __name__ == "__main__":
    unittest.main()
