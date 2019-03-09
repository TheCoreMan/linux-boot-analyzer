import argparse
import datetime
import glob
import json
import os
import platform
import pprint
# todo  from tdqm import tdqm - refrain from this for now, since collector shouldn't depend on frivolous packages.
#  Would be cool thou
import socket

from parsers import UnitParser


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
    elif args.output == "file":
        print("Trying to write output to " + args.output_path)
        with open(args.output_path, "w") as output_file:
            json.dump(final_analysis_report, output_file)
    else:
        raise NotImplementedError(args.output)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Analyze linux boot unit files. Run me on the machine which you want to analyze!')
    parser.add_argument('--systems', '-s', nargs='+', help='Which systems to analyze', default=["systemd"],
                        choices=SYSTEM_TO_UNIT_FILE_GLOB.keys())

    subparsers = parser.add_subparsers(title="output", help="Choose where to output the result to", dest='output')

    subparsers.add_parser("print", help="Print to standard output (useful for debugging).")
    file_output = subparsers.add_parser("file", help="Write to local file.")
    file_output.add_argument("--output_path", "-o", help="Where to output results to",
                             default=os.path.join(os.curdir, "lba.out"))
    # TODO add server

    return parser.parse_args()


SYSTEM_TO_UNIT_FILE_GLOB = {
    "systemd": os.path.join("/", "etc", "systemd", "system", "*service")
}


def get_all_unit_paths_for_system(system):
    return glob.glob(SYSTEM_TO_UNIT_FILE_GLOB[system])


def parse_all_specific_system_units(system):
    unit_files = get_all_unit_paths_for_system(system)

    parsed_units = []
    parser = UnitParser(system)
    for unit_file in unit_files:
        parsed_unit_info = parser.parse_unit(unit_file)
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


def collect_metadata():
    return {
        "target_info": {
            "hostname": socket.gethostname(),
            "kernel": platform.version(),
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "time": datetime.datetime.now().isoformat(" ")
    }


if __name__ == '__main__':
    main()
