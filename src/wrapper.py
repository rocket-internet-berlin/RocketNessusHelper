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
from globs import *

# system imports
import os
import sys
import warnings
#import urllib3
import requests


class Wrapper:
    """ Class for programm wrapper """

    def __init__(self):
        """ init """

        return

    @staticmethod
    def msg(message, verbose=False):
        """ Print message to stdout """

        if not verbose:
            sys.stdout.write('[+] ' + message + '\n')
        else:
            sys.stdout.write('    > ' + message + '\n')

        return

    @staticmethod
    def warn(message):
        """ Print warning message """

        sys.stderr.write('[!] WARNING: ' + message + '\n')

        return

    @staticmethod
    def error(message):
        """ Print error message and exit """

        sys.stderr.write('[-] ERROR: ' + message + '\n')
        sys.exit(1337)

    @staticmethod
    def makeReportDir(outdir):
        """ Make report dir: outdir + date """

        outdir = os.path.join(outdir, TODAY)
        os.makedirs(outdir, exist_ok=True)

        return outdir

    @staticmethod
    def buildUrl(host, port):
        """ Make a base URL """

        return 'https://' + host + ':' + port

    @staticmethod
    def disableWarnings():
        """ Disable annoying SSL related warnings made by requests/urllbi3 """

        #urllib3.disable_warnings()
        requests.packages.urllib3.disable_warnings()
        warnings.filterwarnings(action='ignore', module='requests')

        return


# EOF
