import os
import math
import time
import datetime

################################################################################
# GENERATE LIBERTY VIEW
#
# Generate a .lib file based on the given SRAM.
################################################################################


def write_header(LIB_file, voltage):
    """Writes the Liberty header"""

    # Get the date
    d = datetime.date.today()
    date = d.isoformat()
    current_time = time.strftime("%H:%M:%SZ", time.gmtime())

    LIB_file.write("    technology (cmos);\n")
    LIB_file.write("    delay_model : table_lookup;\n")
    LIB_file.write("    revision : 1.0;\n")
    LIB_file.write('    date : "%s %s";\n' % (date, current_time))
    LIB_file.write('    comment : "SRAM";\n')
    LIB_file.write('    time_unit : "1ns";\n')
    LIB_file.write('    voltage_unit : "1V";\n')
    LIB_file.write('    current_unit : "1uA";\n')
    LIB_file.write('    leakage_power_unit : "1uW";\n')
    LIB_file.write("    nom_process : 1;\n")
    LIB_file.write("    nom_temperature : 25.000;\n")
    LIB_file.write("    nom_voltage : %s;\n" % voltage)
    LIB_file.write("    capacitive_load_unit (1,pf);\n\n")
    LIB_file.write('    pulling_resistance_unit : "1kohm";\n\n')
    LIB_file.write("    operating_conditions(tt_1.0_25.0) {\n")
    LIB_file.write("        process : 1;\n")
    LIB_file.write("        temperature : 25.000;\n")
    LIB_file.write("        voltage : %s;\n" % voltage)
    LIB_file.write("        tree_type : balanced_tree;\n")
    LIB_file.write("    }\n")
    LIB_file.write("\n")


def write_defaults(LIB_file, max_slew):
    """Writes the library defaults"""

    LIB_file.write("    /* default attributes */\n")
    LIB_file.write("    default_cell_leakage_power : 0;\n")
    LIB_file.write("    default_fanout_load : 1;\n")
    LIB_file.write("    default_inout_pin_cap : 0.0;\n")
    LIB_file.write("    default_input_pin_cap : 0.0;\n")
    LIB_file.write("    default_output_pin_cap : 0.0;\n")
    LIB_file.write("    default_input_pin_cap : 0.0;\n")
    LIB_file.write("    default_max_transition : %.3f;\n\n" % max_slew)
    LIB_file.write("    default_operating_conditions : tt_1.0_25.0;\n")
    LIB_file.write("    default_leakage_power_density : 0.0;\n")
    LIB_file.write("\n")

    LIB_file.write("    /* additional header data */\n")
    LIB_file.write("    slew_derate_from_library : 1.000;\n")
    LIB_file.write("    slew_lower_threshold_pct_fall : 20.000;\n")
    LIB_file.write("    slew_upper_threshold_pct_fall : 80.000;\n")
    LIB_file.write("    slew_lower_threshold_pct_rise : 20.000;\n")
    LIB_file.write("    slew_upper_threshold_pct_rise : 80.000;\n")
    LIB_file.write("    input_threshold_pct_fall : 50.000;\n")
    LIB_file.write("    input_threshold_pct_rise : 50.000;\n")
    LIB_file.write("    output_threshold_pct_fall : 50.000;\n")
    LIB_file.write("    output_threshold_pct_rise : 50.000;\n\n")
    LIB_file.write("\n")


def write_table_templates(LIB_file, name):
    """Writes the default table templates"""

    LIB_file.write("    lu_table_template(%s_mem_out_delay_template) {\n" % name)
    LIB_file.write("        variable_1 : input_net_transition;\n")
    LIB_file.write("        variable_2 : total_output_net_capacitance;\n")
    LIB_file.write('            index_1 ("1000, 1001");\n')
    LIB_file.write('            index_2 ("1000, 1001");\n')
    LIB_file.write("    }\n")
    LIB_file.write("    lu_table_template(%s_mem_out_slew_template) {\n" % name)
    LIB_file.write("        variable_1 : total_output_net_capacitance;\n")
    LIB_file.write('            index_1 ("1000, 1001");\n')
    LIB_file.write("    }\n")
    LIB_file.write("    lu_table_template(%s_constraint_template) {\n" % name)
    LIB_file.write("        variable_1 : related_pin_transition;\n")
    LIB_file.write("        variable_2 : constrained_pin_transition;\n")
    LIB_file.write('            index_1 ("1000, 1001");\n')
    LIB_file.write('            index_2 ("1000, 1001");\n')
    LIB_file.write("    }\n")
    LIB_file.write("    power_lut_template(%s_energy_template_clkslew) {\n" % name)
    LIB_file.write("        variable_1 : input_transition_time;\n")
    LIB_file.write('            index_1 ("1000, 1001");\n')
    LIB_file.write("    }\n")
    LIB_file.write("    power_lut_template(%s_energy_template_sigslew) {\n" % name)
    LIB_file.write("        variable_1 : input_transition_time;\n")
    LIB_file.write('            index_1 ("1000, 1001");\n')
    LIB_file.write("    }\n")


def write_bus_defs(LIB_file, name, bits, addr_width):
    """Writes the bus type definitions"""

    addr_width_m1 = addr_width - 1
    LIB_file.write("    type (%s_DATA) {\n" % name)
    LIB_file.write("        base_type : array ;\n")
    LIB_file.write("        data_type : bit ;\n")
    LIB_file.write("        bit_width : %d;\n" % bits)
    LIB_file.write("        bit_from : %d;\n" % (int(bits) - 1))
    LIB_file.write("        bit_to : 0 ;\n")
    LIB_file.write("        downto : true ;\n")
    LIB_file.write("    }\n")
    LIB_file.write("    type (%s_ADDRESS) {\n" % name)
    LIB_file.write("        base_type : array ;\n")
    LIB_file.write("        data_type : bit ;\n")
    LIB_file.write("        bit_width : %d;\n" % addr_width)
    LIB_file.write("        bit_from : %d;\n" % addr_width_m1)
    LIB_file.write("        bit_to : 0 ;\n")
    LIB_file.write("        downto : true ;\n")
    LIB_file.write("    }\n")


def write_int_power_table(LIB_file, rise_fall, template_name, slew_indices, dynamic):
    """Writes the internal power table"""

    LIB_file.write("            %s_power(%s) {\n" % (rise_fall, template_name))
    LIB_file.write('                index_1 ("%s");\n' % slew_indices)
    LIB_file.write('                values ("%.3f, %.3f")\n' % (dynamic, dynamic))
    LIB_file.write("            }\n")


def write_internal_power(LIB_file, template_name, slew_indices, dynamic, when=None):
    """Writes the internal power section"""

    LIB_file.write("        internal_power(){\n")
    if when:
        LIB_file.write('            when : "%s";\n' % when)
    write_int_power_table(LIB_file, "rise", template_name, slew_indices, dynamic)
    write_int_power_table(LIB_file, "fall", template_name, slew_indices, dynamic)
    LIB_file.write("        }\n")


def write_clk_pin(
    LIB_file, name, min_driver_in_cap, min_period, slew_indices, clkpindynamic,
        pin_str="clk"    # <-- ADDED: pin_str default "clk" for single port
):
    """Writes the clock pin section"""

    int_power_template = name + "_energy_template_clkslew"
    LIB_file.write("    pin(clk)   {\n")
    LIB_file.write("        direction : input;\n")
    LIB_file.write("        capacitance : %.3f;\n" % (min_driver_in_cap * 5))
    # Clk pin is usually higher cap for fanout control, assuming an x5 driver.
    LIB_file.write("        clock : true;\n")
    LIB_file.write("        min_period           : %.3f ;\n" % (min_period))
    write_internal_power(LIB_file, int_power_template, slew_indices, clkpindynamic)
    LIB_file.write("    }\n")
    LIB_file.write("\n")


def write_cell_delay(
    LIB_file, rise_fall, template_name, slew_indices, load_indices, delay
):
    """Writes the cell delay section"""

    LIB_file.write("            cell_%s(%s) {\n" % (rise_fall, template_name))
    LIB_file.write('                index_1 ("%s");\n' % slew_indices)
    LIB_file.write('                index_2 ("%s");\n' % load_indices)
    LIB_file.write("                values ( \\\n")
    LIB_file.write('                  "%.3f, %.3f", \\\n' % (delay, delay))
    LIB_file.write('                  "%.3f, %.3f" \\\n' % (delay, delay))
    LIB_file.write("                )\n")
    LIB_file.write("            }\n")


def write_cell_transition(
    LIB_file, rise_fall, template_name, load_indices, min_slew, max_slew
):
    """Writes the cell transition section"""

    LIB_file.write("            %s_transition(%s) {\n" % (rise_fall, template_name))
    LIB_file.write('                index_1 ("%s");\n' % load_indices)
    LIB_file.write('                values ("%.3f, %.3f")\n' % (min_slew, max_slew))
    LIB_file.write("            }\n")


def write_cell_constraint(LIB_file, rise_fall, template_name, slew_indices, val):
    """Writes the cell constraint section"""

    LIB_file.write("            %s_constraint(%s) {\n" % (rise_fall, template_name))
    LIB_file.write('                index_1 ("%s");\n' % slew_indices)
    LIB_file.write('                index_2 ("%s");\n' % slew_indices)
    LIB_file.write("                values ( \\\n")
    LIB_file.write('                  "%.3f, %.3f", \\\n' % (val, val))
    LIB_file.write('                  "%.3f, %.3f" \\\n' % (val, val))
    LIB_file.write("                )\n")
    LIB_file.write("            }\n")


def write_output_bus(
    LIB_file,
    mem,
    name,
    pin_name,
    max_load,
    slew_indices,
    load_indices,
    min_slew,
    max_slew,
    related_clk="clk",
    addr_bus="addr_in"
):
    """Writes the output bus definition"""

    tcq = float(mem.access_time_ns)
    delay_template_name = name + "_mem_out_delay_template"
    transition_template_name = name + "_mem_out_slew_template"

    LIB_file.write("    bus(%s)   {\n" % pin_name)
    LIB_file.write("        bus_type : %s_DATA;\n" % name)
    LIB_file.write("        direction : output;\n")
    LIB_file.write("        max_capacitance : %.3f;\n" % max_load)
    # Based on 32x inverter being a common max (or near max) inverter
    LIB_file.write("        memory_read() {\n")
    LIB_file.write("            address : %s;\n" % addr_bus)
    LIB_file.write("        }\n")
    LIB_file.write("        timing() {\n")
    LIB_file.write('            related_pin : "%s" ;\n' % related_clk)
    LIB_file.write("            timing_type : rising_edge;\n")
    LIB_file.write("            timing_sense : non_unate;\n")
    write_cell_delay(
        LIB_file, "rise", delay_template_name, slew_indices, load_indices, tcq
    )
    write_cell_delay(
        LIB_file, "fall", delay_template_name, slew_indices, load_indices, tcq
    )
    write_cell_transition(
        LIB_file, "rise", transition_template_name, load_indices, min_slew, max_slew
    )
    write_cell_transition(
        LIB_file, "fall", transition_template_name, load_indices, min_slew, max_slew
    )
    LIB_file.write("        }\n")
    LIB_file.write("    }\n")


def write_pin(
    LIB_file,
    name,
    pin_name,
    min_driver_in_cap,
    slew_indices,
    tsetup,
    thold,
    pindynamic,
    related_clk="clk"
):
    """Writes the enable pin definition"""

    template_name = name + "_constraint_template"
    LIB_file.write("    pin(%s){\n" % pin_name)
    LIB_file.write("        direction : input;\n")
    LIB_file.write("        capacitance : %.3f;\n" % (min_driver_in_cap))

    write_timing(LIB_file, name, slew_indices, tsetup, thold, related_clk)
    write_internal_power(
        LIB_file, name + "_energy_template_sigslew", slew_indices, pindynamic
    )
    LIB_file.write("    }\n")


def write_timing(LIB_file, name, slew_indices, tsetup, thold, related_clk):
    """Writes the pin/bus timing section"""

    template_name = name + "_constraint_template"
    LIB_file.write("        timing() {\n")
    LIB_file.write("            related_pin : \"%s\";\n" % related_clk)
    LIB_file.write("            timing_type : setup_rising ;\n")
    write_cell_constraint(LIB_file, "rise", template_name, slew_indices, tsetup)
    write_cell_constraint(LIB_file, "fall", template_name, slew_indices, tsetup)
    LIB_file.write("        } \n")
    LIB_file.write("        timing() {\n")
    LIB_file.write("            related_pin : \"%s\";\n" % related_clk)
    LIB_file.write("            timing_type : hold_rising ;\n")
    write_cell_constraint(LIB_file, "rise", template_name, slew_indices, thold)
    write_cell_constraint(LIB_file, "fall", template_name, slew_indices, thold)
    LIB_file.write("        }\n")


def write_address_bus(
    LIB_file,
    name,
    bus_name,
    min_driver_in_cap,
    slew_indices,
    tsetup,
    thold,
    pindynamic,
    related_clk="clk"  # <-- ADDED
):
    """Writes the address bus"""

    LIB_file.write("    bus(%s)   {\n" % bus_name)
    LIB_file.write("        bus_type : %s_ADDRESS;\n" % name)
    LIB_file.write("        direction : input;\n")
    LIB_file.write("        capacitance : %.3f;\n" % (min_driver_in_cap))
    write_timing(LIB_file, name, slew_indices, tsetup, thold, related_clk)
    write_internal_power(
        LIB_file, name + "_energy_template_sigslew", slew_indices, pindynamic
    )
    LIB_file.write("    }\n")


def write_data_bus(
    LIB_file,
    name,
    bus_name,
    min_driver_in_cap,
    slew_indices,
    tsetup,
    thold,
    pindynamic,
    related_clk="clk", addr_bus="addr_in", we_pin="we_in"
):
    """Writes the data bus"""

    LIB_file.write("    bus(%s)   {\n" % bus_name)
    LIB_file.write("        bus_type : %s_DATA;\n" % name)
    LIB_file.write("        memory_write() {\n")
    LIB_file.write("            address : %s;\n" % addr_bus)
    LIB_file.write("            clocked_on : \"%s\";\n" % related_clk)
    LIB_file.write("        }\n")
    LIB_file.write("        direction : input;\n")
    LIB_file.write("        capacitance : %.3f;\n" % (min_driver_in_cap))
    write_timing(LIB_file, name, slew_indices, tsetup, thold, related_clk)
    write_internal_power(
        LIB_file,
        name + "_energy_template_sigslew",
        slew_indices,
        pindynamic,
        "(! (%s) )" % we_pin
    )
    write_internal_power(
        LIB_file,
        name + "_energy_template_sigslew",
        slew_indices,
        pindynamic,
        "(%s)" % we_pin
    )
    LIB_file.write("    }\n")


def write_cell(
    LIB_file,
    mem,
    name,
    bits,
    addr_width,
    min_driver_in_cap,
    min_load,
    max_load,
    num_rwport,
    min_slew,
    max_slew,
):
    """Writes the Liberty cell"""

    area = float(mem.area_um2)
    tsetup = float(mem.t_setup_ns)
    thold = float(mem.t_hold_ns)
    min_period = float(mem.cycle_time_ns)
    clkpindynamic = float(mem.pin_dynamic_power_mW) * 1e3
    pindynamic = float(mem.pin_dynamic_power_mW) * 1e1
    leakage = float(mem.standby_leakage_per_bank_mW) * 1e3

    slew_indices = "%.3f, %.3f" % (min_slew, max_slew)
    # input pin transition with between 1xfo4 and 100xfo4
    load_indices = "%.3f, %.3f" % (min_load, max_load)
    # output capacitance table between a 1x and 32x inverter

    LIB_file.write("cell(%s) {\n" % name)
    LIB_file.write("    area : %.3f;\n" % area)
    LIB_file.write("    interface_timing : true;\n")
    LIB_file.write("    memory() {\n")
    LIB_file.write("        type : ram;\n")
    LIB_file.write("        address_width : %d;\n" % addr_width)
    LIB_file.write("        word_width : %d;\n" % bits)
    LIB_file.write("    }\n")

    # single-port
    if num_rwport == 1:
        write_clk_pin(
            LIB_file, name, min_driver_in_cap, min_period, slew_indices, clkpindynamic
        )
        write_output_bus(
            LIB_file,
            mem,
            name,
            "rd_out",
            max_load,
            slew_indices,
            load_indices,
            min_slew,
            max_slew,
        )
        write_pin(
            LIB_file,
            name,
            "we_in",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
        )
        write_pin(
            LIB_file,
            name,
            "ce_in",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
        )
        write_address_bus(
            LIB_file,
            name,
            "addr_in",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
        )
        write_data_bus(
            LIB_file,
            name,
            "wd_in",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
        )

    # <-- ADDED begin
    # dual-port
    elif num_rwport == 2:
        # port0
        write_clk_pin(LIB_file, name, min_driver_in_cap, min_period, slew_indices, clkpindynamic, "clk0")
        write_output_bus(
            LIB_file,
            mem,
            name,
            "rd_out0",
            max_load,
            slew_indices,
            load_indices,
            min_slew,
            max_slew,
            related_clk="clk0",
            addr_bus="addr_in0"
        )
        write_pin(
            LIB_file,
            name,
            "we_in0",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
            "clk0",
        )
        write_pin(
            LIB_file,
            name,
            "ce_in0",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
            "clk0",
        )
        write_address_bus(
            LIB_file,
            name,
            "addr_in0",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
            "clk0",
        )
        write_data_bus(
            LIB_file,
            name,
            "wd_in0",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
            "clk0",
            "addr_in0",
            "we_in0"
        )
        # port1
        write_clk_pin(LIB_file, name, min_driver_in_cap, min_period, slew_indices, clkpindynamic, "clk1")
        write_output_bus(
            LIB_file,
            mem,
            name,
            "rd_out1",
            max_load,
            slew_indices,
            load_indices,
            min_slew,
            max_slew,
            related_clk="clk1",
            addr_bus="addr_in1"
        )
        write_pin(
            LIB_file,
            name,
            "we_in1",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
            "clk1",
        )
        write_pin(
            LIB_file,
            name,
            "ce_in1",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
            "clk1",
        )
        write_address_bus(
            LIB_file,
            name,
            "addr_in1",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
            "clk1",
        )
        write_data_bus(
            LIB_file,
            name,
            "wd_in1",
            min_driver_in_cap,
            slew_indices,
            tsetup,
            thold,
            pindynamic,
            "clk1",
            "addr_in1",
            "we_in1"
        )
    # <-- ADDED end

    LIB_file.write("    cell_leakage_power : %.3f;\n" % (leakage))
    LIB_file.write("}\n")


def create_lib(mem, results_dir):
    """Writes the Liberty lib"""

    # Make sure the data types are correct
    name = str(mem.name)
    bits = int(mem.width_in_bits)
    min_driver_in_cap = float(mem.cap_input_pf)
    fo4 = float(mem.fo4_ps) / 1e3

    # Only support 1RW srams. At some point, expose these as well!
    num_rwport = mem.rw_ports

    # Number of bits for address
    addr_width = math.ceil(math.log2(mem.depth))

    # TODO: Arbitrary indices for the NLDM table. This is used for Clk->Q arcs
    # as well as setup/hold times. We only have a single value for these, there
    # are two options. 1. adding some sort of static variation of the single
    # value for each table entry, 2. use the same value so all interpolated
    # values are the same. The 1st is more realistic but depend on good variation
    # values which is process sepcific and I don't have a strategy for
    # determining decent variation values without breaking NDA so right now we
    # have no variations.
    #
    # The table indices are main min/max values for interpolation. The tools
    # typically don't like extrapolation so a large range is nice, but makes the
    # single value strategy described above even more unrealistic.
    #
    min_slew = 1 * fo4
    # arbitrary (1x fo4, fear that 0 would cause issues)
    max_slew = 25 * fo4
    # arbitrary (25x fo4 as ~100x fanout ... i know that is not really how it works)
    min_load = 1 * min_driver_in_cap
    # arbitrary (1x driver, fear that 0 would cause issues)
    max_load = 100 * min_driver_in_cap
    # arbitrary (100x driver)

    # Start generating the LIB file

    LIB_file = open(os.sep.join([results_dir, name + ".lib"]), "w")

    LIB_file.write("library(%s) {\n" % name)
    write_header(LIB_file, float(mem.process.voltage))
    write_defaults(LIB_file, max_slew)
    write_table_templates(LIB_file, name)
    LIB_file.write("    library_features(report_delay_calculation);\n")
    write_bus_defs(LIB_file, name, bits, addr_width)
    write_cell(
        LIB_file,
        mem,
        name,
        bits,
        addr_width,
        min_driver_in_cap,
        min_load,
        max_load,
        num_rwport,
        min_slew,
        max_slew,
    )
    LIB_file.write("\n")
    LIB_file.write("}\n")

    LIB_file.close()
