import glob
import os
import pprint

from parsers import UnitParser


def main():
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
    pprint.pprint(parsed_units)


if __name__ == '__main__':
    main()
