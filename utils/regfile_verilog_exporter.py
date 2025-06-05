#!/usr/bin/env python3

from verilog_exporter import VerilogExporter


class RegFileVerilogExporter(VerilogExporter):
    """Reg file verilog exporter"""

    def __init__(self, memory):
        """Initializer"""
        VerilogExporter.__init__(self, memory)

    def export_module(self, out_fh):
        """Exports the verilog module to the output stream"""

        mem = self.get_memory()
        out_fh.write(f"module {mem.get_name()}\n")
        out_fh.write("(\n")
        for i in range(0, self.get_memory().get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.write_rw_port_decl_set(suffix, out_fh)
        out_fh.write("    clk,\n")
        out_fh.write(");\n")
        out_fh.write(f"    parameter DATA_WIDTH = {mem.get_width()};\n")
        out_fh.write(f"    parameter ADDR_WIDTH = {mem.get_addr_width()};\n")
        out_fh.write("\n")
        for i in range(0, self.get_memory().get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.write_rw_port_defn_set(suffix, out_fh)
        out_fh.write("    input  wire                     clk,\n")
        out_fh.write("\n")
        out_fh.write(
            f"    // Memory array: {mem.get_depth()} words of {mem.get_width()} bits\n"
        )
        out_fh.write("    reg [DATA_WIDTH-1:0] mem [0:(1 << ADDR_WIDTH)-1];\n")
        out_fh.write("\n")
        for i in range(0, mem.get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.write_rw_port_always(suffix, out_fh)
        out_fh.write("endmodule\n")

    def write_rw_port_always(self, suffix, out_fh):
        """Writes the always @ section for the port group"""

        out_fh.write(f"    // Synchronous Port {suffix.upper()}\n")
        out_fh.write("     always @(posedge clk) begin\n")
        out_fh.write(f"        if (we_{suffix}) begin\n")
        out_fh.write(f"            mem[addr_{suffix}] <= din_{suffix};\n")
        out_fh.write("        end\n")
        out_fh.write(
            f"        dout_{suffix} <= mem[addr_{suffix}];  // Read occurs after write (read-after-write OK)\n"
        )
        out_fh.write("    end\n")
        out_fh.write("\n")
