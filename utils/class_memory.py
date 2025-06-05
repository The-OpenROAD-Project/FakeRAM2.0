#!/usr/bin/env python3

import math
import argparse

from physical_data import PhysicalData
from lef_exporter import LefExporter

################################################################################
# MEMORY CLASS
#
# This class stores the information about a specific memory that is being
# generated. This class takes in a process object, the information in one of
# the items in the "sram" list section of the json configuration file
################################################################################


class Memory:
    def __init__(self, name, width_in_bits, depth, num_banks, process, timing_data):
        """
        Initializer

        Stores the process and timing_data objects directly on the memory, so
        that they can be accessed by the appropriate exporters. The physical
        data stores anything related to LEF.
        """

        self.process = process
        self.name = name
        self.width_in_bits = width_in_bits
        self.depth = depth
        self.addr_width = math.ceil(math.log2(self.depth))
        self.num_banks = num_banks
        self.width_in_bytes = math.ceil(self.width_in_bits / 8.0)
        self.total_size = self.width_in_bytes * self.depth
        self.timing_data = timing_data
        self.physical = PhysicalData()
        (width_um, height_um) = self.process.get_macro_dimensions(
            self.width_in_bits, self.depth, self.num_banks
        )
        self.physical.set_extents(width_um, height_um)
        self.physical.snap_to_grid(
            self.process.snap_width_nm, self.process.snap_height_nm
        )
        if False:  # pragma: no cover
            print("Total Bitcell Height is", self.height_um)
            print("Total Bitcell Width is", self.width_um)
        num_pins = self.get_num_pins()
        self.physical.set_pin_pitches(
            self.name, num_pins, self.process.pin_pitch_um, self.process.y_offset
        )

    def get_name(self):
        """Returns the name of the memory"""
        return self.name

    def get_depth(self):
        """Returns the depth"""
        return self.depth

    def get_width(self):
        """Returns the width in bits"""
        return self.width_in_bits

    def get_num_banks(self):
        """Returns the number of banks"""
        return self.num_banks

    def get_width_in_bytes(self):
        """Returns the width in bytes"""
        return self.width_in_bytes

    def get_total_size(self):
        """Returns the total size in bytes"""
        return self.total_size

    def get_data_bus_msb(self):
        """
        Returns the data bus MSB, which is one less than the data bus width
        """
        return self.get_width() - 1

    def get_addr_width(self):
        """Returns the address width"""
        return self.addr_width

    def get_addr_bus_msb(self):
        """
        Returns the address bus MSB, which is one less than the address bus
        width
        """

        return self.get_addr_width() - 1

    def get_process_data(self):
        """Returns the process data"""
        return self.process

    def get_timing_data(self):
        """Returns the timing data"""
        return self.timing_data

    def get_physical_data(self):
        """Returns the physical data"""
        return self.physical

    def get_num_rw_ports(self):
        """Returns the number of rw ports"""
        return self.num_rw_ports

    def write_lef_file(self, out_file_name):
        """Writes the LEF content to a file"""

        exporter = LefExporter(self)
        exporter.export_file(out_file_name)

    @staticmethod
    def main(memory_type, port_config):  # pragma: nocover
        from run_utils import RunUtils
        from class_process import Process
        from timing_data import TimingData
        from memory_factory import MemoryFactory

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-c", "--config_file", help="FakeRAM config file", required=True
        )
        parser.add_argument(
            "-w", "--width", help="memory width in bits", type=int, required=True
        )
        parser.add_argument(
            "-d", "--depth", help="memory depth", type=int, required=True
        )
        parser.add_argument(
            "-b",
            "--banks",
            choices=[1, 2, 4],
            type=int,
            required=True,
            help="number of banks",
        )
        parser.add_argument("-n", "--name", help="memory name", required=True)
        parser.add_argument("-o", "--output_dir", default=".", help="Output directory")
        args = parser.parse_args()

        json_data = RunUtils.get_config(args.config_file)
        timing_data = TimingData(json_data)
        process_data = Process(json_data)
        memory = MemoryFactory.create(
            args.name,
            int(args.width),
            int(args.depth),
            int(args.banks),
            memory_type,
            port_config,
            process_data,
            timing_data,
        )
        RunUtils.write_memory(memory, args.output_dir)
