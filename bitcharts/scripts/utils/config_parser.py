# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser


class Parser(SafeConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


def config_parser(config_file):
    f = Parser()
    f.read(config_file)
    return f.as_dict()
