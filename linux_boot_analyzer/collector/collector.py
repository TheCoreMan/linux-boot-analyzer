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


import requests
from common import SYSTEM_TO_UNIT_FILE_GLOB
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
    elif args.output == "server":
        server_host = args.IP + ":" + args.port
        url = "http://" + server_host + "/report_analysis"  # TODO extract to common
        print("Trying to write output to " + url)
        requests.post(url, json=final_analysis_report)
    else:
        raise NotImplementedError(args.output)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Analyze linux boot unit files. Run me on the machine which you want to analyze!')

    subparsers = parser.add_subparsers(title="output", help="Choose where to output the result to", dest='output')

    print_parser = subparsers.add_parser("print", help="Print to standard output (useful for debugging).")
    print_parser.add_argument('-s', '--systems', nargs='+', help='Which systems to analyze', default=["systemd"],
                              choices=SYSTEM_TO_UNIT_FILE_GLOB.keys())
    file_parser = subparsers.add_parser("file", help="Write to local file.")
    file_parser.add_argument("--output_path", "-o", help="Where to output results to",
                             default=os.path.join(os.curdir, "lba.out"))
    file_parser.add_argument('-s', '--systems', nargs='+', help='Which systems to analyze', default=["systemd"],
                             choices=SYSTEM_TO_UNIT_FILE_GLOB.keys())
    
    server_output = subparsers.add_parser("server", help="Send to remote DB server.")
    server_output.add_argument("IP", help="IP address of server")
    server_output.add_argument("port", help="Port of the server")
    server_output.add_argument('-s', '--systems', nargs='+', help='Which systems to analyze', default=["systemd"],
                             choices=SYSTEM_TO_UNIT_FILE_GLOB.keys())

    return parser.parse_args()


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
