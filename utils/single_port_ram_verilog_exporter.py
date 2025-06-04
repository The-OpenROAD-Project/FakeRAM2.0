#!/usr/bin/env python3

from verilog_exporter import VerilogExporter


class SinglePortRAMVerilogExporter(VerilogExporter):
    """
    Single port RAM verilog exporter. Differs from others for backward
    compatibility
    """

    def __init__(self, memory):
        """Initializer"""
        VerilogExporter.__init__(self, memory)

    def export_module(self, out_fh):
        """Exports the verilog module to the output stream"""

        mem = self.get_memory()
        out_fh.write(f"module {mem.get_name()}\n")
        self.write_module_ports(out_fh)
        out_fh.write("   reg    [BITS-1:0]        mem [0:WORD_DEPTH-1];\n")
        out_fh.write("\n")
        out_fh.write("   integer j;\n")
        out_fh.write("\n")
        out_fh.write("   always @(posedge clk)\n")
        out_fh.write("   begin\n")
        out_fh.write("      if (ce_in)\n")
        out_fh.write("      begin\n")
        out_fh.write(
            "         //if ((we_in !== 1'b1 && we_in !== 1'b0) && corrupt_mem_on_X_p)\n"
        )
        out_fh.write("         if (corrupt_mem_on_X_p &&\n")
        out_fh.write("             ((^we_in === 1'bx) || (^addr_in === 1'bx))\n")
        out_fh.write("            )\n")
        out_fh.write("         begin\n")
        out_fh.write(
            "            // WEN or ADDR is unknown, so corrupt entire array (using unsynthesizeable for loop)\n"
        )
        out_fh.write("            for (j = 0; j < WORD_DEPTH; j = j + 1)\n")
        out_fh.write("               mem[j] <= 'x;\n")
        out_fh.write(
            '            $display("warning: ce_in=1, we_in is %b, addr_in = %x in '
            + mem.get_name()
            + '", we_in, addr_in);\n'
        )
        out_fh.write("         end\n")
        out_fh.write("         else if (we_in)\n")
        out_fh.write("         begin\n")
        out_fh.write("            mem[addr_in] <= (wd_in) | (mem[addr_in]);\n")
        out_fh.write("         end\n")
        out_fh.write("         // read\n")
        out_fh.write("         rd_out <= mem[addr_in];\n")
        out_fh.write("      end\n")
        out_fh.write("      else\n")
        out_fh.write("      begin\n")
        out_fh.write("         // Make sure read fails if ce_in is low\n")
        out_fh.write("         rd_out <= 'x;\n")
        out_fh.write("      end\n")
        out_fh.write("   end\n")
        out_fh.write("\n")
        self.write_timing_check(out_fh)
        out_fh.write("endmodule\n")

    def write_module_ports(self, out_fh):
        """Writes the module port declarations"""

        mem = self.get_memory()
        out_fh.write("(\n")
        out_fh.write("   rd_out,\n")
        out_fh.write("   addr_in,\n")
        out_fh.write("   we_in,\n")
        out_fh.write("   wd_in,\n")
        out_fh.write("   clk,\n")
        out_fh.write("   ce_in\n")
        out_fh.write(");\n")
        out_fh.write(f"   parameter BITS = {mem.get_width()};\n")
        out_fh.write(f"   parameter WORD_DEPTH = {mem.get_depth()};\n")
        out_fh.write(f"   parameter ADDR_WIDTH = {mem.get_addr_width()};\n")
        out_fh.write(f"   parameter corrupt_mem_on_X_p = 1;\n")
        out_fh.write("\n")
        out_fh.write("   output reg [BITS-1:0]    rd_out;\n")
        out_fh.write("   input  [ADDR_WIDTH-1:0]  addr_in;\n")
        out_fh.write("   input                    we_in;\n")
        out_fh.write("   input  [BITS-1:0]        wd_in;\n")
        out_fh.write("   input                    clk;\n")
        out_fh.write("   input                    ce_in;\n")
        out_fh.write("\n")

    def write_timing_check(self, out_fh):
        """Writes timing check placeholder data"""

        out_fh.write(
            "   // Timing check placeholders (will be replaced during SDF back-annotation)\n"
        )
        out_fh.write("   reg notifier;\n")
        out_fh.write("   specify\n")
        out_fh.write("      // Delay from clk to rd_out\n")
        out_fh.write("      (posedge clk *> rd_out) = (0, 0);\n")
        out_fh.write("\n")
        out_fh.write("      // Timing checks\n")
        out_fh.write("      $width     (posedge clk,            0, 0, notifier);\n")
        out_fh.write("      $width     (negedge clk,            0, 0, notifier);\n")
        out_fh.write("      $period    (posedge clk,            0,    notifier);\n")
        out_fh.write("      $setuphold (posedge clk, we_in,     0, 0, notifier);\n")
        out_fh.write("      $setuphold (posedge clk, ce_in,     0, 0, notifier);\n")
        out_fh.write("      $setuphold (posedge clk, addr_in,   0, 0, notifier);\n")
        out_fh.write("      $setuphold (posedge clk, wd_in,     0, 0, notifier);\n")
        out_fh.write("   endspecify\n")
        out_fh.write("\n")

    def export_blackbox(self, out_fh):
        """Exports the SystemVerilog blackbox to the output stream"""

        mem = self.get_memory()
        addr_bus_msb = mem.get_addr_bus_msb()
        data_bus_msb = mem.get_data_bus_msb()
        self.export_bb_header(out_fh)
        out_fh.write(f"   output reg [31:0] rd_out,\n")
        out_fh.write(f"   input [{addr_bus_msb}:0] addr_in,\n")
        out_fh.write("   input we_in,\n")
        out_fh.write(f"   input [{data_bus_msb}:0] wd_in,\n")
        out_fh.write("   input clk,\n")
        out_fh.write("   input ce_in\n")
        self.export_bb_footer(out_fh)
