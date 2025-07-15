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
        for index, rw_port_group in enumerate(mem.get_rw_port_groups()):
            self.write_rw_port_decl_set(rw_port_group, out_fh, index)
        out_fh.write("\n);\n")
        out_fh.write(f"    parameter DATA_WIDTH = {mem.get_width()};\n")
        out_fh.write(f"    parameter ADDR_WIDTH = {mem.get_addr_width()};\n")
        out_fh.write("\n")
        for rw_port_group in self.get_memory().get_rw_port_groups():
            self.write_rw_port_defn_set(rw_port_group, out_fh)
        out_fh.write("\n")
        out_fh.write(
            f"    // Memory array: {mem.get_depth()} words of {mem.get_width()} bits\n"
        )
        out_fh.write("    reg [DATA_WIDTH-1:0] mem [0:(1 << ADDR_WIDTH)-1];\n")
        out_fh.write("\n")
        for rw_port_group in self.get_memory().get_rw_port_groups():
            self.write_rw_port_always(rw_port_group, out_fh)
        out_fh.write("endmodule\n")

    def write_rw_port_always(self, rw_port_group, out_fh):
        """Writes the always @ section for the port group"""

        suffix = rw_port_group.get_suffix()
        clk_pin_name = rw_port_group.get_clock_name()
        out_fh.write(f"    // Synchronous Port {suffix.upper()}\n")
        out_fh.write(f"     always @(posedge {clk_pin_name}) begin\n")
        out_fh.write(f"        if ({rw_port_group.get_write_enable_name()}) begin\n")
        out_fh.write(
            f"            mem[{rw_port_group.get_address_bus_name()}] <= {rw_port_group.get_data_input_bus_name()};\n"
        )
        out_fh.write("        end\n")
        out_fh.write(
            f"        {rw_port_group.get_data_output_bus_name()} <= mem[{rw_port_group.get_address_bus_name()}];  // Read occurs after write (read-after-write OK)\n"
        )
        out_fh.write("    end\n")
        out_fh.write("\n")
