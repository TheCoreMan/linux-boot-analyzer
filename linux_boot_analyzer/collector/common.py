import os

SYSTEM_TO_UNIT_FILE_GLOB = {
    "systemd": os.path.join("/", "etc", "systemd", "system", "*service"),
    "sysv": os.path.join("/", "etc", "init.d", "*")
}
