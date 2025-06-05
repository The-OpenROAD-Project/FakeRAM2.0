#!/usr/bin/env python3

import sys
import argparse

from utils.run_utils import RunUtils
from utils.class_process import Process
from utils.memory_factory import MemoryFactory
from utils.timing_data import TimingData


def get_args() -> argparse.Namespace:
    """
    Get command line arguments
    """
    parser = argparse.ArgumentParser(
        description="""
    This project is designed to generate black-boxed SRAMs for use in CAD
    flows where either an SRAM generator is not available or doesn't
    exist.  """
    )
    parser.add_argument("config", help="JSON configuration file")
    parser.add_argument(
        "--output_dir",
        action="store",
        help="Output directory ",
        required=False,
        default="results",
    )
    return parser.parse_args()


def get_memory_type(json_data):
    if "memory_type" in json_data:
        return json_data["memory_type"]
    return "RAM"


def get_port_config(json_data):
    if "port_configuration" in json_data:
        return json_data["port_configuration"]
    return "SP"


def main(args: argparse.Namespace):
    json_data = RunUtils.get_config(args.config)
    # Create a process object (shared by all srams)
    process = Process(json_data)
    timing_data = TimingData(json_data)

    memory_type = get_memory_type(json_data)
    port_config = get_port_config(json_data)

    # Go through each sram and generate the lib, lef and v files
    for sram_data in json_data["srams"]:
        name = str(sram_data["name"])
        width_in_bits = int(sram_data["width"])
        depth = int(sram_data["depth"])
        num_banks = int(sram_data["banks"])
        memory = MemoryFactory.create(
            name,
            width_in_bits,
            depth,
            num_banks,
            memory_type,
            port_config,
            process,
            timing_data,
        )
        RunUtils.write_memory(memory, args.output_dir)


### Entry point
if __name__ == "__main__":
    args = get_args()
    main(args)
