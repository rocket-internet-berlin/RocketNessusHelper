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
import os
import datetime


# nessus-helper version number
NESSUS_HELPER_VERSION='0.4'

# nessus-helper root path (dirty hack)
ROOT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

# dates
TODAY = str(datetime.date.today())
YESTERDAY = str(datetime.date.fromordinal(datetime.date.today().toordinal()-1))

# nessus-helper actions
ACTIONS=['report', 'summary']

# EOF
