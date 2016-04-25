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
from globs import *

# system imports
import argparse


class ArgsParser:
    """ command line argument parsing """

    def __init__(self):
        """ init """

        return

    @staticmethod
    def parseArgs():
        """ Parse command line arguments and options """

        parser = argparse.ArgumentParser(usage='%(prog)s -n | -m [options]',
                add_help=False)
        parser.add_argument(
                '-h',
                metavar='<host>',
                dest='nessus_host',
                help='nessus host'
                )
        parser.add_argument(
                '-p',
                metavar='<port>',
                dest='nessus_port',
                default='8834',
                help='nessus port (default: 8834)'
                )
        parser.add_argument(
                '-l',
                metavar='<login>',
                dest='nessus_login',
                help='nessus login (format: user:pass)'
                )
        parser.add_argument(
                '-c',
                metavar='<config>',
                dest='config',
                default=ROOT_PATH+'/config/nessus-helper.ini',
                help='path to ini config file (default: '
                'config/nessus-helper.ini)'
                )
        parser.add_argument(
                '-n',
                metavar='<action>',
                dest='action',
                help='choose action to perform - ? to list actions'
                )
        parser.add_argument(
                '-s',
                metavar='<sec>',
                dest='sleep',
                default=5,
                help='seconds to sleep before downloading reports (default: 5)'
                )
        parser.add_argument(
                '-m',
                dest='mail',
                action='store_true',
                help='send reports via mail'
                )
        parser.add_argument(
                '-f',
                metavar='<format>',
                dest='format',
                default='html',
                help='format of the reports: html, pdf (default: html)'
                )
        parser.add_argument(
                '-o',
                metavar='<outdir>',
                dest='outdir',
                default=ROOT_PATH+'/nessus-reports',
                help='output directory for reports (default: nessus-reports)'
                )
        parser.add_argument(
                '-v',
                action='store_true',
                default=False,
                help='verbose mode'
                )
        parser.add_argument(
                '-V',
                action='version',
                version='%(prog)s v' + NESSUS_HELPER_VERSION,
                help='print version information'
                )
        parser.add_argument(
                '-H',
                action='help',
                help='print this help message'
                )

        return(parser.parse_args())


# EOF
