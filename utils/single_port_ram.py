#!/usr/bin/env python3
#
# The Verilog, LEF and Liberty output for the single port RAM matches the
# previous implementation for backward compatibility
#

from class_memory import Memory
from ram import RAM
from single_port_ram_verilog_exporter import SinglePortRAMVerilogExporter
from single_port_ram_liberty_exporter import SinglePortRAMLibertyExporter
from single_port_ram_lef_exporter import SinglePortRAMLefExporter


class SinglePortRAM(RAM):
    """
    Class for single port RAM

    RAM has the following pins/busses

    output [DATA_WIDTH-1:0]  rd_out
    input  [ADDR_WIDTH-1:0]  addr_in
    input                    we_in
    input  [DATA_WIDTH-1:0]  wd_in
    input                    clk
    input                    ce_in
    """

    def __init__(
        self, name, width_in_bits, depth, num_banks, process_data, timing_data
    ):
        """Initializer"""
        RAM.__init__(
            self, name, width_in_bits, depth, num_banks, process_data, timing_data
        )
        self.num_rw_ports = 1

    def get_num_pins(self):
        """Returns the total number of logical pins"""
        # rd_out (#bits) + wd_in (#bits) + addr_in (#addr_width) + we_in/ce_in/clk
        return (2 * self.get_width()) + self.get_addr_width() + 3

    def write_verilog_file(self, out_file_name, is_blackbox=False):
        """
        Writes a verilog file

        If is_blackbox is set, it writes just the port declarations and a
        blackbox pragma. Otherwise, it writes the full RTL.
        """
        exporter = SinglePortRAMVerilogExporter(self)
        exporter.export_file(out_file_name, is_blackbox)

    def write_liberty_file(self, out_file_name):
        """Writes a Liberty file"""
        exporter = SinglePortRAMLibertyExporter(self)
        exporter.export_file(out_file_name)

    def write_lef_file(self, out_file_name):
        """Writes a LEF file"""
        exporter = SinglePortRAMLefExporter(self)
        exporter.export_file(out_file_name)


if __name__ == "__main__":  # pragma: nocover
    Memory.main("RAM", "SP")
