#!/usr/bin/env python3

import os
import sys
import math
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from class_memory import Memory
from class_process import Process
from test_utils import TestUtils


class MemoryTest(unittest.TestCase):
    """Unit test for Memory object"""

    def setUp(self):
        """Sets up process object used by test methods"""

        self._process = Process(TestUtils.get_base_process_data())
        # delta for use when comparing floats
        self._delta = 0.01
        self._sram_data = {
            "name": "sample",
            "width": 39,
            "depth": 2048,
            "banks": 1,
        }

    def test_memory(self):
        """
        Tests basic memory object
        """

        memory = Memory(self._process, self._sram_data)
        self.assertEqual(memory.name, self._sram_data["name"])
        self.assertEqual(memory.width_in_bits, self._sram_data["width"])
        self.assertEqual(memory.depth, self._sram_data["depth"])
        self.assertEqual(memory.num_banks, self._sram_data["banks"])
        self.assertEqual(memory.cache_type, "cache")
        self.assertEqual(memory.width_in_bytes, math.ceil(memory.width_in_bits / 8.0))
        self.assertEqual(memory.total_size, memory.width_in_bytes * memory.depth)
        # the area is calculated prior to snapping, so check that the area is
        # within some area determined by the snap area
        area_delta = self._process.snap_width_nm * self._process.snap_height_nm * 1e-3
        self.assertAlmostEqual(
            memory.area_um2, memory.width_um * memory.height_um, delta=area_delta)

        # These values are all hard-coded in the Memory object
        self.assertEqual(memory.rw_ports, 1)
        self.assertEqual(memory.tech_node_nm, 7)
        self.assertEqual(memory.associativity, 1)
        self.assertEqual(memory.t_setup_ns, 0.05)
        self.assertEqual(memory.t_hold_ns, 0.05)
        self.assertEqual(memory.standby_leakage_per_bank_mW, 0.1289)
        self.assertEqual(memory.access_time_ns, 0.2183)
        self.assertEqual(memory.pin_dynamic_power_mW, 0.0013449)
        self.assertEqual(memory.cap_input_pf, 0.005)
        self.assertEqual(memory.cycle_time_ns, 0.1566)
        self.assertEqual(memory.fo4_ps, 9.0632)


if __name__ == "__main__":
    unittest.main()
