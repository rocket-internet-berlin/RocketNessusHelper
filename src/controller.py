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
from wrapper import Wrapper
from mail import Mail
from check import Check
from usage import Usage
from parser import ArgsParser
from iniconfig import IniConfig
from nessus import Nessus

# system imports
import os
import sys
import time
import datetime


class Controller:
    """ Program flow controller """

    def __init__(self):
        """ init """

        self.opts = None        # All options for nessus-helper
        self.ini = None         # ini-configuration data

        return

    def getOptions(self):
        """ Get additional options and values """

        # nessus
        if not self.opts['nessus_host']:
            self.opts['nessus_host'] = self.ini.config.get('nessus', 'host')
            self.opts['nessus_port'] = self.ini.config.get('nessus', 'port')
        self.opts['nessus_url'] = Wrapper.buildUrl(self.opts['nessus_host'],
                self.opts['nessus_port'])
        self.opts['nessus_login'] = self.getNessusLogin()
        self.opts['nessus_chapters'] = self.ini.config.get('nessus', 'chapters')

        # smtp
        self.opts['smtp_login'] = {}
        self.opts['smtp_login']['user'] = self.ini.config.get('mail', 'user')
        self.opts['smtp_login']['pass'] = self.ini.config.get('mail', 'pass')
        self.opts['smtp_host'] = self.ini.config.get('mail', 'host')
        self.opts['smtp_port'] = self.ini.config.get('mail', 'port')
        self.opts['smtp_from'] = self.ini.config.get('mail', 'from')

        # addressbook
        self.opts['addrbook'] = self.ini.config.options('addressbook')

        return

    def getNessusLogin(self):
        """ get Nessus login from cmdline or read from ini config file """

        login = {}

        if self.opts['nessus_login']:
            login['user'] = self.opts['nessus_login'].split(':')[0]
            login['pass'] = self.opts['nessus_login'].split(':')[1]
        elif self.ini.config['nessus']:
            login['user'] = self.ini.config.get('nessus', 'user')
            login['pass'] = self.ini.config.get('nessus', 'pass')
        else:
            Wrapper.error('no login specified')

        return login

    def sendReports(self, option):
        """ Send out reports via email """

        msg = {}        # mail header and body
        mail = ''
        server = {}     # smtp server
        m = Mail()

        # smtp server address and tcp port
        server['addr'] = self.opts['smtp_host']
        server['port'] = self.opts['smtp_port']

        # smtp (static content) read from ini file
        msg['from'] = self.opts['smtp_from']

        Wrapper.msg('Sending out reports')

        if option == 'report':
            # for each report in report directory except summary.txt
            for f in os.listdir(self.opts['outdir'] + '/' + TODAY):
                if f != 'summary.txt':
                    report = self.opts['outdir'] + '/' + TODAY + '/' + f
                    name = f.split('.')[0]

                    # mail header + body
                    msg['message'] = 'Hi,\n\nplease find attached the Nessus ' \
                            'report for this week.\n\nBest Regards,\n\n' \
                            "Rocket Internet's Security Team"
                    msg['subject'] = '[{0}] Your new Nessus report for {1} ' \
                            'is ready'.format(name, TODAY)
                    msg['to'] = self.ini.config.get('addressbook', name)

                    # build and send mail
                    mail = m.buildMail(msg, (report,))
                    m.sendMail(server, mail, self.opts['smtp_login'], tls=True)
        else:
            report = self.opts['outdir'] + '/' + TODAY + '/' + 'summary.txt'
            with open(report, 'r') as f:
                report_data = f.read()

            # mail header + body
            msg['message'] = 'Hi,\n\nplease find below the Nessus ' \
                    'Summary Report for this week:\n\n'
            msg['message'] += report_data
            msg['message'] += "\n\nBest Regards,\n\nRocket Internet's " \
                    "Security Team"
            msg['subject'] = 'Nessus Summary Report ({0})'.format(TODAY)
            msg['to'] = self.ini.config.get('addressbook', 'Summary')

            # build and send mail
            mail = m.buildMail(msg, (report,))
            m.sendMail(server, mail, self.opts['smtp_login'], tls=True)

        return

    def processReports(self, option):
        """ Login to nessus, export and download nessus- or summary-reports """

        names = []

        Wrapper.msg('Login to Nessus on ' + "'" + self.opts['nessus_url'] + "'")
        nessus = Nessus(self.opts['nessus_url'])
        nessus.login(self.opts['nessus_login']['user'],
                self.opts['nessus_login']['pass'])
        if not nessus.login:
            Wrapper.error('Cannot login in to Nessus')

        # get scan lists
        Wrapper.msg('Fetching the scan lists')
        scan_list = nessus.getScanList()

        # export and download nessus reports
        if option == 'report':
            Wrapper.msg('Exporting and downloading reports')
            outdir = Wrapper.makeReportDir(self.opts['outdir'])

            for scan in scan_list['scans']:
                if scan['name'] in self.opts['addrbook']:
                    if scan['status'] == 'completed':
                        scan_details = nessus.getScan(scan['id'])
                        end_date = datetime.datetime.fromtimestamp(
                                int(scan_details['info']['scan_end'])
                                ).strftime('%Y-%m-%d')
                        if end_date == TODAY or end_date == YESTERDAY:
                            for root, dirs, files in os.walk(
                                    self.opts['outdir'] + '/' + YESTERDAY):
                                names.append(files)
                            for root, dirs, files in os.walk(
                                    self.opts['outdir'] + '/' + TODAY):
                                names.append(files)
                            names = [i for sublist in names for i in sublist]

                            if scan['name'] + '.html' not in names:
                                file_id = nessus.exportScanResult(scan['id'],
                                        self.opts['format'],
                                        self.opts['nessus_chapters'])['file']

                                # wait before downloading reports if status is
                                # not OK
                                if not nessus.exportStatusCheck(scan['id'],
                                        file_id):
                                    time.sleep(int(self.opts['sleep']))

                                nessus.downloadReport(scan['id'], file_id,
                                        self.opts['format'], scan['name'],
                                        outdir)
        # create and download summary
        else:
            Wrapper.msg('Creating the summary report')
            outdir = Wrapper.makeReportDir(self.opts['outdir'])

            for scan in scan_list['scans']:
                if scan['name'] in self.opts['addrbook']:
                    if scan['status'] == 'completed':
                        scan_res = nessus.getScan(scan['id'])
                        for h in range(len(scan_res['hosts'])):
                            host_id = scan_res['hosts'][h]['host_id']
                            res = nessus.getHostDetails(scan['id'], host_id)
                            for r in res['vulnerabilities']:
                                # critical, high, medium
                                if r['severity'] in (4, 3, 2):
                                    with open(os.path.join(outdir, 'summary.txt'), 'a') as f:
                                        f.write('project: ' + scan['name'] +
                                                ' host: ' + r['hostname'] +
                                                ' issue: ' + r['plugin_name'] + '\n')


        # logout of nessus
        Wrapper.msg('Logout of nessusd')
        nessus.logout()

        return

    def start(self):
        """ All program flow is handled here """

        # usage, init, checks
        Usage.banner()
        args = ArgsParser.parseArgs()
        self.opts = vars(args)
        Check.checkArgc()
        Check.checkArgs(['-n', '-m'])
        Check.checkActions(self.opts['action'])
        Check.checkReportFormat(self.opts['format'])

        # ini config
        Wrapper.msg("Reading configuration file " + "'" +
                self.opts['config'] + "'")
        self.ini = IniConfig(self.opts['config'])
        self.ini.readConfig()
        Check.checkIniFile(self.ini.config)

        # additional options from config file
        self.getOptions()

        ### nessus actions ###

        # nessus report
        if self.opts['action'] in ACTIONS:
            self.processReports(self.opts['action'])

        # send reports
        if self.opts['mail']:
            if self.opts['action'] in ACTIONS:
                self.sendReports(self.opts['action'])

        return

    def end(self):
        """ Epilog """

        Wrapper.msg('Game Over')

        return


# EOF
