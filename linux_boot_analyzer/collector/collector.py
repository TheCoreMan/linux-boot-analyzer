import argparse
import glob
import os
import pprint

from parsers import UnitParser


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze linux boot unit files.')
    parser.add_argument('output', 
                        choices=['print', 'file', 'server'],
                        help='Where to output to')
    return parser.parse_args()


def main():
    args = parse_args()
    parsed_units = parse_all_units()
    if args.output == "print":
        pprint.pprint(parsed_units)
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
