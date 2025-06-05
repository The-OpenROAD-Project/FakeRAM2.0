#!/usr/bin/env python3

from class_memory import Memory
from ram import RAM


class DualPortRAM(RAM):
    """
    Class for dual port RAM

    RAM has the following pins/busses

    input                      we_a,
    input  [ADDR_WIDTH-1:0]    addr_a,
    input  [DATA_WIDTH-1:0]    din_a,
    output [DATA_WIDTH-1:0]    dout_a,
    input                      we_b,
    input  [ADDR_WIDTH-1:0]    addr_b,
    input  [DATA_WIDTH-1:0]    din_b,
    output [DATA_WIDTH-1:0]    dout_b,
    input                      clk,
    """

    def __init__(
        self, name, width_in_bits, depth, num_banks, process_data, timing_data
    ):
        """Initializer"""
        RAM.__init__(
            self, name, width_in_bits, depth, num_banks, process_data, timing_data
        )
        self.num_rw_ports = 2

    def get_num_pins(self):
        """Returns the total number of logical pins"""

        # din (#bits) + dout (#bits) + addr (#addr_width) + we
        rw_port_group_size = (2 * self.get_width()) + self.get_addr_width() + 1
        # 2 rw groups + clk
        return (2 * rw_port_group_size) + 1


if __name__ == "__main__":  # pragma: nocover
    Memory.main("RAM", "DP")
