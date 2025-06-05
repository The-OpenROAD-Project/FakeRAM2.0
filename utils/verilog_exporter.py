#!/usr/bin/env python3

from exporter import Exporter


class VerilogExporter(Exporter):
    """Verilog exporter base"""

    def __init__(self, memory):
        """Initializer"""

        Exporter.__init__(self, memory)

    def export_file(self, file_name, is_blackbox=False):
        """
        Exports the verilog content to a file.

        If is_blackbox, only write the port definitions. Otherwise, write the
        full RTL
        """

        with open(file_name, "w") as out_fh:
            self.export(out_fh, is_blackbox)

    def export(self, out_fh, is_blackbox=False):
        """
        Exports the verilog content to an output stream.

        If is_blackbox, only write the port definitions. Otherwise, write the
        full RTL
        """
        if is_blackbox:
            self.export_blackbox(out_fh)
        else:
            self.export_module(out_fh)

    # -------------- Utilities --------------
    def write_rw_port_decl_set(self, suffix, out_fh):
        """Writes the RW port group declarations"""

        out_fh.write(f"    we_{suffix},\n")
        out_fh.write(f"    addr_{suffix},\n")
        out_fh.write(f"    din_{suffix},\n")
        out_fh.write(f"    dout_{suffix},\n")

    def write_rw_port_defn_set(self, suffix, out_fh):
        """Writes the RW port group definitions"""

        out_fh.write(f"    // Port {suffix.upper()}\n")
        out_fh.write(f"    input  wire                     we_{suffix},\n")
        out_fh.write(f"    input  wire [ADDR_WIDTH-1:0]    addr_{suffix},\n")
        out_fh.write(f"    input  wire [DATA_WIDTH-1:0]    din_{suffix},\n")
        out_fh.write(f"    output reg  [DATA_WIDTH-1:0]    dout_{suffix},\n")
        out_fh.write("\n")

    def export_bb_header(self, out_fh):
        """Writes the SystemVerilog blackbox header"""

        out_fh.write("(* blackbox *)\n")
        out_fh.write("module {} (\n".format(self.get_memory().get_name()))

    def export_bb_footer(self, out_fh):
        """Writes the SystemVerilog blackbox footer"""

        out_fh.write(");\n")
        out_fh.write("endmodule\n")

    def export_bb_port_decl_set(self, suffix, out_fh):
        """Writes the SystemVerilog port declarations"""

        mem = self.get_memory()
        addr_bus_msb = mem.get_addr_bus_msb()
        data_bus_msb = mem.get_data_bus_msb()
        out_fh.write(f"    input we_{suffix},\n")
        out_fh.write(f"    input [{addr_bus_msb}:0] addr_{suffix},\n")
        out_fh.write(f"    input [{data_bus_msb}:0] din_{suffix},\n")
        out_fh.write(f"    output reg [{data_bus_msb}:0] dout_{suffix},\n")

    def export_blackbox(self, out_fh):
        """Writes the blackbox content to the output stream"""

        self.export_bb_header(out_fh)
        for i in range(0, self.get_memory().get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.export_bb_port_decl_set(suffix, out_fh)
        out_fh.write("    clk,\n")
        self.export_bb_footer(out_fh)
