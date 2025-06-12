#!/usr/bin/env python3

from verilog_exporter import VerilogExporter


class RAMVerilogExporter(VerilogExporter):
    """RAM verilog exporter"""

    def __init__(self, memory):
        """Initializer"""
        VerilogExporter.__init__(self, memory)

    def export_module(self, out_fh):
        """Exports the verilog module to the output stream"""

        mem = self.get_memory()
        out_fh.write(f"module {mem.get_name()}\n")
        out_fh.write("(\n")
        for i in range(0, mem.get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.write_rw_port_decl_set(suffix, out_fh)
        out_fh.write("    clk\n")
        out_fh.write(");\n")
        out_fh.write(f"    parameter DATA_WIDTH = {mem.get_width()};\n")
        out_fh.write(f"    parameter ADDR_WIDTH = {mem.get_addr_width()};\n")
        out_fh.write("\n")
        for i in range(0, mem.get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.write_rw_port_defn_set(suffix, out_fh)
        out_fh.write("    input  wire                     clk,\n")
        out_fh.write("\n")
        out_fh.write(
            f"    // Memory array: {mem.get_depth()} words of {mem.get_width()} bits\n"
        )
        out_fh.write("    reg [DATA_WIDTH-1:0] mem [0:(1 << ADDR_WIDTH)-1];\n")
        out_fh.write("\n")
        out_fh.write("    // Registers for synchronous reads\n")
        out_fh.write("    reg [ADDR_WIDTH-1:0] addr_a_reg;\n")
        out_fh.write("    reg [ADDR_WIDTH-1:0] addr_b_reg;\n")
        out_fh.write("\n")
        out_fh.write("    integer i;\n")
        out_fh.write("\n")
        out_fh.write("    always @(posedge clk) begin\n")
        for i in range(0, mem.get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.write_rw_port_always(suffix, out_fh)
        out_fh.write("        // Synchronous readback\n")
        for i in range(0, mem.get_num_rw_ports()):
            suffix = chr(ord("a") + i)
            self.write_readback(suffix, out_fh)
        out_fh.write("    end\n")
        out_fh.write("endmodule\n")

    def write_rw_port_always(self, suffix, out_fh):
        """Writes the always @ section for the port group"""

        out_fh.write(f"        // ==== Port {suffix.upper()} write ====\n")
        out_fh.write(
            f"        if (^we_{suffix} === 1'bx || ^addr_{suffix} === 1'bx) begin\n"
        )
        out_fh.write(
            "            // Unknown write enable or address ? corrupt entire memory\n"
        )
        out_fh.write("            for (i = 0; i < (1 << ADDR_WIDTH); i = i + 1)\n")
        out_fh.write("                mem[i] <= {DATA_WIDTH{1'bx}};\n")
        out_fh.write(f"        end else if (we_{suffix}) begin\n")
        out_fh.write(f"            mem[addr_{suffix}] <= din_{suffix};\n")
        out_fh.write("        end\n")

    def write_readback(self, suffix, out_fh):
        """Writes readback section for the port group"""

        out_fh.write(f"        addr_{suffix}_reg <= addr_{suffix};\n")
        out_fh.write(f"        dout_{suffix} <= mem[addr_{suffix}_reg];\n")
