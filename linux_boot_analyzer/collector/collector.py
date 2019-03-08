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
    parsed_units = parse_all_units()
    metadata = collect_metadata()
    final_analysis_report = {
        "metadata": metadata,
        "units": parsed_units
    }
    if args.output == "print":
        pprint.pprint(final_analysis_report)
    else:
        raise NotImplementedError(args.output)


def parse_all_units():
    path_to_systemd_unit_files = os.path.join("/", "etc", "systemd", "system", "*service")
    systemd_service_files = glob.glob(path_to_systemd_unit_files)
    parsed_units = []
    for service_file in systemd_service_files:
        parser = UnitParser()
        parsed_unit_info = parser.parse_unit(service_file, "systemd")
        parsed_units.append(
            {
                "path": service_file,
                "inner_info": parsed_unit_info
            }
        )
    return parsed_units


if __name__ == '__main__':
    main()
