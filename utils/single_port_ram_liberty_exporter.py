#!/usr/bin/env python3

from ram_liberty_exporter import RAMLibertyExporter


class SinglePortRAMLibertyExporter(RAMLibertyExporter):
    """
    Liberty exporter for single port SRAM. It differs from the others due to
    pin differences, which were kept for backward compatibility
    """

    def __init__(self, memory):
        """Initializer"""
        RAMLibertyExporter.__init__(self, memory)

    def write_cell(self, out_fh):
        """Writes the Liberty cell"""

        name = self._memory.get_name()
        clk_pin_name = "clk"
        timing_data = self._memory.get_timing_data()
        self.write_memory_section(out_fh)
        self.write_clk_pin(clk_pin_name, out_fh)
        self.write_output_bus(out_fh, name, "rd_out", clk_pin_name, True)
        self.write_pin(out_fh, name, "we_in", clk_pin_name)
        self.write_pin(out_fh, name, "ce_in", clk_pin_name)
        self.write_address_bus(out_fh, name, "addr_in", clk_pin_name)
        self.write_data_bus(out_fh, name, "wd_in", clk_pin_name, "we_in", True)
