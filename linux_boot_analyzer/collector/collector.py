import glob
import os


def main():
    print("hi")
    path_to_systemd_unit_files = os.path.join("etc", "systemd", "system")
    service_files = glob.glob(os.path.join(path_to_systemd_unit_files, "*.service"))
    for service_file in service_files:
        print(service_file)


if __name__ == '__main__':
    main()
