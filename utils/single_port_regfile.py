#!/usr/bin/env python3

from class_memory import Memory
from reg_file import RegFile


class SinglePortRegFile(RegFile):
    """
    Class for single port register file

    Reg file has the following pins/busses

    input                      we_a,
    input  [ADDR_WIDTH-1:0]    addr_a,
    input  [DATA_WIDTH-1:0]    din_a,
    output [DATA_WIDTH-1:0]    dout_a,
    input                      clk,
    """

    def __init__(
        self, name, width_in_bits, depth, num_banks, process_data, timing_data
    ):
        """Initializer"""
        RegFile.__init__(
            self, name, width_in_bits, depth, num_banks, process_data, timing_data
        )
        self.num_rw_ports = 1

    def get_num_pins(self):
        """Returns the total number of logical pins"""
        # din (#bits) + dout (#bits) + addr (#addr_width) + we/clk
        return (2 * self.get_width()) + self.get_addr_width() + 2


if __name__ == "__main__":  # pragma: nocover
    Memory.main("RF", "SP")
