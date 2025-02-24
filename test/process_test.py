#!/usr/bin/env python3

import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from class_process import Process


class ProcessTest(unittest.TestCase):
    """Unit test for Process class"""

    def setUp(self):
        """Sets up base_data with example config data"""

        self._base_data = {
            "tech_nm": 7,
            "voltage": 0.7,
            "metal_prefix": "M",
            "metal_layer": "M4",
            "pin_width_nm": 24,
            "pin_pitch_nm": 48,
            "metal_track_pitch_nm": 48,
            "contacted_poly_pitch_nm": 54,
            "column_mux_factor": 1,
            "fin_pitch_nm": 27,
            "manufacturing_grid_nm": 1,
            "snap_width_nm": 190,
            "snap_height_nm": 1400,
        }

    def test_process(self):
        """Tests process fields based on example config"""

        process = Process(self._base_data)
        self.assertIsNotNone(process)
        self.assertEqual(process.tech_nm, self._base_data["tech_nm"])
        self.assertTrue(isinstance(process.voltage, str))
        self.assertEqual(process.voltage, str(self._base_data["voltage"]))
        self.assertEqual(process.metal_prefix, self._base_data["metal_prefix"])
        self.assertEqual(process.metal_layer, self._base_data["metal_layer"])
        self.assertEqual(process.pin_width_nm, self._base_data["pin_width_nm"])
        self.assertEqual(process.pin_pitch_nm, self._base_data["pin_pitch_nm"])
        self.assertEqual(
            process.metal_track_pitch_nm, self._base_data["metal_track_pitch_nm"]
        )
        self.assertEqual(
            process.contacted_poly_pitch_nm, self._base_data["contacted_poly_pitch_nm"]
        )
        self.assertEqual(process.fin_pitch_nm, self._base_data["fin_pitch_nm"])
        self.assertEqual(
            process.manufacturing_grid_nm, self._base_data["manufacturing_grid_nm"]
        )
        self.assertEqual(process.snap_width_nm, self._base_data["snap_width_nm"])
        self.assertEqual(process.snap_height_nm, self._base_data["snap_height_nm"])
        # check nm -> um
        self.assertEqual(process.tech_um, process.tech_nm / 1000.0)
        self.assertEqual(process.pin_width_um, process.pin_width_nm / 1000.0)
        self.assertEqual(process.pin_pitch_um, process.pin_pitch_nm / 1000.0)
        self.assertEqual(
            process.metal_track_pitch_um, process.metal_track_pitch_nm / 1000.0
        )
        self.assertEqual(
            process.manufacturing_grid_um, process.manufacturing_grid_nm / 1000.0
        )

    def test_process_optional_snap(self):
        """Tests defaulting when snap_width and snap_height are not defined"""

        process_data = self._base_data.copy()
        del process_data["snap_width_nm"]
        del process_data["snap_height_nm"]
        process = Process(process_data)
        self.assertEqual(process.tech_nm, self._base_data["tech_nm"])
        self.assertEqual(process.voltage, str(self._base_data["voltage"]))
        self.assertEqual(process.metal_prefix, self._base_data["metal_prefix"])
        self.assertEqual(process.metal_layer, self._base_data["metal_layer"])
        self.assertEqual(process.pin_width_nm, self._base_data["pin_width_nm"])
        self.assertEqual(process.pin_pitch_nm, self._base_data["pin_pitch_nm"])
        self.assertEqual(
            process.metal_track_pitch_nm, self._base_data["metal_track_pitch_nm"]
        )
        self.assertEqual(
            process.contacted_poly_pitch_nm, self._base_data["contacted_poly_pitch_nm"]
        )
        self.assertEqual(process.fin_pitch_nm, self._base_data["fin_pitch_nm"])
        self.assertEqual(
            process.manufacturing_grid_nm, self._base_data["manufacturing_grid_nm"]
        )
        self.assertEqual(process.snap_width_nm, 1)
        self.assertEqual(process.snap_height_nm, 1)

    def test_process_misaligned_pin_mfg_grid_pitch(self):
        """
        Tests detection that pin pitch is not a multiple of the metal track
        pitch
        """
        process_data = self._base_data.copy()
        process_data["pin_pitch_nm"] = 54
        process_data["metal_track_pitch_nm"] = 6
        process_data["manufacturing_grid_nm"] = 5

        with self.assertRaises(Exception):
            process = Process(process_data)

    def test_process_misaligned_pin_track_pitch(self):
        """
        Tests detection that pin pitch is not a multiple of the metal track
        pitch
        """

        process_data = self._base_data.copy()
        process_data["pin_pitch_nm"] = 54
        process_data["metal_track_pitch_nm"] = 5

        with self.assertRaises(Exception):
            process = Process(process_data)


if __name__ == "__main__":
    unittest.main()
