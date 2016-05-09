#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Nessus Helper
:copyright: (c) 2016 Rocket Internet SE
:license: MIT, see LICENSE for more details.
"""

__author__ = "Levon Kayan"
__email__ = "levon.kayan@rocket-internet.de"

# own imports
from wrapper import Wrapper
from globs import *

# system imports
import sys


class Check:
    """ program and program usage check routines """

    def __init__(self):
        """ init """

        return

    @staticmethod
    def checkArgc():
        """ Check argument count """

        if len(sys.argv) == 1:
            Wrapper.error('-H for help and usage')

        return

    @staticmethod
    def checkArgs(args):
        """ Check if required arguments are given """

        length = len(args)

        for a in args:
            if a not in sys.argv:
                length -= 1
                if length is 0:
                    Wrapper.error('Wrong usage. -H for help.')

        return

    @staticmethod
    def checkActions(action):
        """ Check if chosen action is valid. Print actions if '?' given. """

        if action == '?':
            Wrapper.msg('Available actions: \n')
            Wrapper.msg('report     - export and download nessus reports',
                    verbose=True)
            Wrapper.msg('summary    - create and download a summary report\n',
                    verbose=True)
            sys.exit(1337)

        if action not in ACTIONS:
            Wrapper.error('Please select a correct action')

        return

    @staticmethod
    def checkReportFormat(rformat):
        """ Check if chosen report format exists """

        formats = ('html', 'pdf')

        if rformat not in formats:
            Wrapper.error('Wrong report format: %s' % rformat)

        return

    @staticmethod
    def checkIniFile(ini):
        """ Check ini file configuration """

        sections = ini.sections()

        if not sections:
            Wrapper.error('Cannot read from ini file. Empty or wrong path?')

        check = ('nessus', 'mail', 'addressbook')

        for s in sections:
            if s not in check:
                Wrapper.warn('Missing or wrong section: [%s]' % s)

        return


# EOF
