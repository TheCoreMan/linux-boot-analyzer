import configparser
import hashlib
from collections import OrderedDict


def file_as_bytes(file):
    with file:
        return file.read()


class UnitParser:
    def parse_unit(self, path, system):
        # Todo currently this is some sort of a factory method for ease of extendability. Need to improve this class's
        #  design - for testability of different parsers, probably inject method. Read on factory DP in python
        if system == "systemd":
            parsed = parse_systemd(path)

            results = {
                "system": "systemd",
                "Description": parsed["Unit"]["Description"],
                "ExecStart": parsed["Service"]["ExecStart"],
                # todo this is probably memory inefficent, but meh.
                "md5": hashlib.md5(file_as_bytes(open(path, 'rb'))).hexdigest(),
                "sha-256": hashlib.sha256(file_as_bytes(open(path, 'rb'))).hexdigest()
            }

            if "User" in parsed["Service"]:
                results["User"] = parsed["Service"]["User"]
            if "Group" in parsed["Service"]:
                results["User"] = parsed["Service"]["Group"]

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
