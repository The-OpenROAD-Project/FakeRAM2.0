#!/usr/bin/env python3

from liberty_exporter import LibertyExporter


class RegFileLibertyExporter(LibertyExporter):
    """Reg file Liberty Exporter"""

    def __init__(self, memory):
        """Initializer"""
        LibertyExporter.__init__(self, memory)

    def write_cell(self, out_fh):
        """
        Writes the Liberty cell

        Difference is that we pass False to the rw_pin_set writer to indicate
        that this isn't a RAM.
        """

        name = self._memory.get_name()
        for i in range(0, self._memory.get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.write_rw_pin_set(out_fh, name, suffix, False)
        self.write_clk_pin(out_fh)
