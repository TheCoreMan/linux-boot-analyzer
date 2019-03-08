import argparse
import datetime
import glob
import os
import platform
import pprint
# todo  from tdqm import tdqm - refrain from this for now, since collector shouldn't depend on frivolous packages.
#  Would be cool thou
import socket

from parsers import UnitParser


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze linux boot unit files. Run me on the machine which you want '
                                                 'to analyze!')
    parser.add_argument('output', choices=['print', 'file', 'server'], help='Where to output to')
    parser.add_argument('--systems', '-s', nargs='+', help='Which systems to analyze', default=["systemd"])
    return parser.parse_args()


def collect_metadata():
    return {
        "hostname": socket.gethostname(),
        "kernel": platform.version(),
        "uname": platform.uname(),
        "time": datetime.datetime.now()
    }


def main():
    args = parse_args()
    parsed_units = parse_all_units_in(args.systems)
    metadata = collect_metadata()
    final_analysis_report = {
        "metadata": metadata,
        "units": parsed_units
    }
    if args.output == "print":
        pprint.pprint(final_analysis_report)
    else:
        raise NotImplementedError(args.output)


SYSTEM_TO_UNIT_FILE_GLOB = {
    "systemd": os.path.join("/", "etc", "systemd", "system", "*service")
}


def get_all_unit_paths_for_system(system):
    return glob.glob(SYSTEM_TO_UNIT_FILE_GLOB[system])


def parse_all_specific_system_units(system):
    unit_files = get_all_unit_paths_for_system(system)

    parsed_units = []
    for unit_file in unit_files:
        parser = UnitParser()
        parsed_unit_info = parser.parse_unit(unit_file, system)
        parsed_units.append(
            {
                "path": unit_file,
                "inner_info": parsed_unit_info
            }
        )
    return parsed_units


def parse_all_units_in(systems):
    parsed_units = []
    for system in systems:
        parsed_units += parse_all_specific_system_units(system)
    return parsed_units


if __name__ == '__main__':
    main()
