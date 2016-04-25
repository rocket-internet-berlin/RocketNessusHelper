#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Nessus Helper
:copyright: (c) 2016 Rocket Internet SE
:license: GPLv3+, see LICENSE for more details.
"""

__author__ = "Levon Kayan"
__email__ = "levon.kayan@rocket-internet.de"

# own imports

# system imports
import configparser


class IniConfig:
    """ Ini configuration file handler """

    def __init__(self, inifile):
        """ init """

        self.inifile = inifile
        self.config = configparser.ConfigParser()
        self.config.optionxform = lambda option: option

        return

    def readConfig(self):
        """ Read ini file configuration. Get all sections and key:values """

        self.config.read(self.inifile)

        return


# EOF
