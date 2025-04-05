import os
import sys
import math

from area import get_macro_dimensions

################################################################################
# MEMORY CLASS
#
# This class stores the information about a specific memory that is being
# generated. This class takes in a process object, the information in one of
# the items in the "sram" list section of the json configuration file
################################################################################


class Memory:

    def __init__(self, process, sram_data):

        self.process = process
        self.name = str(sram_data["name"])
        self.width_in_bits = int(sram_data["width"])
        self.depth = int(sram_data["depth"])
        self.num_banks = int(sram_data["banks"])
        self.cache_type = str(sram_data["type"]) if "type" in sram_data else "cache"
        self.rw_ports = int(sram_data["rw_ports"]) if "rw_ports" in sram_data else 1
        self.width_in_bytes = math.ceil(self.width_in_bits / 8.0)
        self.total_size = self.width_in_bytes * self.depth

        self.tech_node_nm = 7

        self.height_um, self.width_um = get_macro_dimensions(process, sram_data)
        self.area_um2 = self.width_um * self.height_um

        self.tech_node_um = self.tech_node_nm / 1000.0

        # Adjust to snap
        self.width_um = (
            math.ceil((self.width_um * 1000.0) / self.process.snap_width_nm)
            * self.process.snap_width_nm
        ) / 1000.0
        self.height_um = (
            math.ceil((self.height_um * 1000.0) / self.process.snap_height_nm)
            * self.process.snap_height_nm
        ) / 1000.0
        if False:  # pragma: no cover
            print("Total Bitcell Height is", self.height_um)
            print("Total Bitcell Width is", self.width_um)

        ## DUMMY (FOR NOW) VALUES FOR LIB CREATION
        self.t_setup_ns = 0.050
        # arbitrary 50ps setup
        self.t_hold_ns = 0.050
        # arbitrary 50ps hold
        self.standby_leakage_per_bank_mW = 0.1289
        self.access_time_ns = 0.2183
        self.pin_dynamic_power_mW = 0.0013449
        self.cap_input_pf = 0.005
        self.cycle_time_ns = 0.1566
        self.fo4_ps = 9.0632
