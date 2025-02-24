#!/usr/bin/env python3

import os
import sys
import json
import argparse
from pathlib import Path

from utils.class_process import Process
from utils.class_memory import Memory

from utils.create_lib import create_lib
from utils.create_lef import create_lef
from utils.create_verilog import create_verilog

################################################################################
# RUN GENERATOR
#
# This is the main part of the script. It will read in the JSON configuration
# file, create a Cacti configuration file, run Cacti, extract the data from
# Cacti, and then generate the timing, physical and logical views for each SRAM
# found in the JSON configuration file.
################################################################################


def get_args() -> argparse.Namespace:
    """
    Get command line arguments
    """
    parser = argparse.ArgumentParser(
        description="""
    BSG Black-box SRAM Generator --
    This project is designed to generate black-boxed SRAMs for use in CAD
    flows where either an SRAM generator is not avaible or doesn't
    exist.  """
    )
    parser.add_argument("config", help="JSON configuration file")
    parser.add_argument(
        "--output_dir",
        action="store",
        help="Output directory ",
        required=False,
        default=None,
    )
    return parser.parse_args()


def ensure_results_dir(output_dir, memory_name):
    if output_dir:  # Output dir was set by command line option
        p = str(Path(output_dir).expanduser().resolve(strict=False))
        results_dir = os.sep.join([p, memory_name])
    else:
        results_dir = os.sep.join([os.getcwd(), "results", memory_name])
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    return results_dir


def main(args: argparse.Namespace):

    # Load the JSON configuration file
    with open(args.config, "r") as fid:
        raw = [line.strip() for line in fid if not line.strip().startswith("#")]
    json_data = json.loads("\n".join(raw))

    # Create a process object (shared by all srams)
    process = Process(json_data)

    # Go through each sram and generate the lib, lef and v files
    for sram_data in json_data["srams"]:
        memory = Memory(process, sram_data)
        results_dir = ensure_results_dir(args.output_dir, memory.name)
        create_lib(memory, results_dir)
        create_lef(memory, results_dir)
        create_verilog(memory, results_dir)


### Entry point
if __name__ == "__main__":
    args = get_args()
    main(args)
