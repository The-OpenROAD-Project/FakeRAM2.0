#!/usr/bin/env python3

from lef_exporter import LefExporter


class SinglePortRAMLefExporter(LefExporter):
    """
    The single port RAM has different port names, since they were kept for
    backward compatibility reasons. So, it needs its own create_signal_pins
    method to account for the names
    """

    def __init__(self, memory):
        """Initializer"""
        LefExporter.__init__(self, memory)

    def create_signal_pins(self, fid, pin_pitch, group_pitch):
        """LEF SIGNAL PINS"""

        mem = self.get_memory()
        bits = mem.get_width()
        y_step = mem.get_process_data().y_step
        y_step = self.write_signal_bus(fid, "rd_out", bits, False, y_step, pin_pitch)
        y_step += group_pitch
        y_step = self.write_signal_bus(fid, "wd_in", bits, True, y_step, pin_pitch)
        y_step += group_pitch
        y_step = self.write_signal_bus(
            fid, "addr_in", mem.get_addr_width(), True, y_step, pin_pitch
        )
        y_step += group_pitch
        y_step = self.add_pin(fid, "we_in", True, y_step, pin_pitch)
        y_step = self.add_pin(fid, "ce_in", True, y_step, pin_pitch)
        y_step = self.add_pin(fid, "clk", True, y_step, pin_pitch)
