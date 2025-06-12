#!/usr/bin/env python3

from class_memory import Memory
from reg_file import RegFile


class DualPortRegFile(RegFile):
    """
    Class for dual port register file

    Reg file has the following pins/busses

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

    def __init__(self, mem_config, process_data, timing_data):
        """
        Initializer

        Parameters:
        mem_config (MemoryConfig): memory parameter container
        process_data (Process): process data container
        timing_data (TimingData): timing data container
        """
        RegFile.__init__(self, mem_config, process_data, timing_data)
        self.num_rw_ports = 2

    def get_num_pins(self):
        """Returns the total number of logical pins"""

        # din (#bits) + dout (#bits) + addr (#addr_width) + we
        rw_port_group_size = (2 * self.get_width()) + self.get_addr_width() + 1
        # 2 rw groups + clk
        return (2 * rw_port_group_size) + 1


if __name__ == "__main__":  # pragma: nocover
    Memory.main("RF", "DP")
