import configparser
from collections import OrderedDict


class UnitParser:
    def parse_unit(self, path, system):
        # Sort of a factory method for ease of extendability
        if system == "systemd":
            parsed = parse_systemd(path)
            return {
                "system": "systemd",
                "Description": parsed["Unit"]["Description"],
                "ExecStart": parsed["Service"]["ExecStart"]
            }


class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            # super(MultiOrderedDict, self).__setitem__(key, value)
            super().__setitem__(key, value)


def parse_systemd(path):
    config = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)
    # cp = configparser.ConfigParser()
    config.read([path])
    return config
