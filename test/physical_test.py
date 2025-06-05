#!/usr/bin/env python3

import os
import sys
import math
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from physical_data import PhysicalData


class PhysicalDataTest(unittest.TestCase):
    """Unit test for PhysicalData class"""

    def setUp(self):
        """Sets up base_data with example config data"""


    def test_empty_physical(self):
        """Tests physical field defaults"""

        physical = PhysicalData()
        self.assertIsNone(physical.get_width())
        self.assertIsNone(physical.get_height())
        self.assertIsNone(physical.get_width(True))
        self.assertIsNone(physical.get_height(True))
        self.assertIsNone(physical.get_pin_pitch())
        self.assertIsNone(physical.get_group_pitch())

    def test_set_extents_and_snapping(self):
        """Tests physical field defaults"""

        physical = PhysicalData()
        width = 123.4
        height = 456.5
        snapped_width = math.ceil(width)
        snapped_height = math.ceil(height)

        # Can't snap before setting extents
        with self.assertRaises(Exception):
            physical.snap_to_grid(1000, 1000)
            
        # Set extents and verify values
        physical.set_extents(width, height)
        self.assertEqual(physical.get_width(False), width)
        self.assertEqual(physical.get_height(False), height)
        self.assertEqual(physical.get_area(False), width * height)
        # Not snapped yet, so should return non-snapped value
        self.assertEqual(physical.get_width(True), width)
        self.assertEqual(physical.get_height(True), height)
        self.assertEqual(physical.get_area(True), width * height)

        # Snap to 1um
        physical.snap_to_grid(1000, 1000)

        # Non-snapped should return original
        self.assertEqual(physical.get_width(False), width)
        self.assertEqual(physical.get_height(False), height)
        self.assertEqual(physical.get_area(False), width * height)
        self.assertEqual(physical.get_width(True), snapped_width)
        self.assertEqual(physical.get_height(True), snapped_height)
        self.assertEqual(physical.get_area(True), snapped_width * snapped_height)

    def test_pin_pitches_exception(self):
        """Tests get_pin_pitches when there's no enough room for the pins"""

        num_pins = 523
        min_pin_pitch = 0.048
        y_offset = 0.048
        height = 21.0
        physical = PhysicalData()

        # Can't set pin pitches before setting height
        with self.assertRaises(Exception):
            physical.set_pin_pitches("bogus", num_pins, min_pin_pitch, y_offset)
            
        # Try again after setting height
        physical.set_extents(height, height)
        physical.snap_to_grid(1, 1)
        with self.assertRaises(Exception):
            physical.set_pin_pitches("bogus", num_pins, min_pin_pitch, y_offset)
    
        
if __name__ == "__main__":
    unittest.main()
