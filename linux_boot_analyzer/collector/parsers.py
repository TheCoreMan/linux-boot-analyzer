import configparser
import hashlib
from collections import OrderedDict

import common


def file_as_bytes(file):
    with file:
        return file.read()


class UnitParser:
    system = ""

    def __init__(self, system):
        if system in common.SYSTEM_TO_UNIT_FILE_GLOB:
            self.system = system
        else:
            raise NotImplementedError()

    def parse_unit(self, path):
        # Todo currently this is some sort of a factory method for ease of extendability. Need to improve this class's
        #  design - for testability of different parsers, probably inject method. Read on factory DP in python
        results = {
            "system": self.system,
            # todo this is probably memory inefficent, but meh.
            "hashes": {
                "md5": hashlib.md5(file_as_bytes(open(path, 'rb'))).hexdigest(),
                "sha-256": hashlib.sha256(file_as_bytes(open(path, 'rb'))).hexdigest()
            }
        }
        if self.system == "systemd":
            parsed = parse_systemd(path)

            results["Description"] = parsed["Unit"]["Description"]
            results["ExecStart"] = parsed["Service"]["ExecStart"]
            results["ImagePath"] = parsed["Service"]["ExecStart"].split()[0]
            try:
                results["ExecHash"] = hashlib.sha256(file_as_bytes(open(results["ImagePath"], 'rb'))).hexdigest()
            except IOError as err:
                pass  # Might be permissions or nonexistant file.
                # TODO add logging mechanism to collector.
            if "User" in parsed["Service"]:
                results["User"] = parsed["Service"]["User"]
            if "Group" in parsed["Service"]:
                results["User"] = parsed["Service"]["Group"]

        # todo elif self.system == "sysv": shlex and parse the executable from the "start" directive if exists.

        return results


class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super().__setitem__(key, value)


def parse_systemd(path):
    config = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)
    config.read([path])
    return config
