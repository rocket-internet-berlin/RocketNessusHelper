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
from wrapper import Wrapper

# system imports
import os
import sys
import json
import requests


class Nessus:
    """ Nessus handler class """

    def __init__(self, url):
        """ init """

        self.url = url
        self.token = ''

        Wrapper.disableWarnings()

        return

    def sendRequest(self, method, resource, data='', token='', verify=False):
        """ Send a request to nessus based on the specified data """

        resource = self.url + resource
        headers = { 'X-Cookie': 'token={0}'.format(self.token),
                    'Content-Type': 'application/json' }
        data = json.dumps(data)

        if method == 'POST':
            r = requests.post(resource, data=data, headers=headers,
                    verify=verify)
        elif method == 'PUT':
            r = requests.put(resource, data=data, headers=headers,
                    verify=verify)
        elif method == 'DELETE':
            r = requests.delete(resource, data=data, headers=headers,
                    verify=verify)
        else:
            r = requests.get(resource, params=data, headers=headers,
                    verify=verify)

        if r.status_code != 200:
            e = r.json()
            Wrapper.error(e['error'])

        if 'download' in resource:
            return r.content
        # temp dirty fix. TODO: make it better
        elif 'session' in resource and method == 'DELETE':
            return
        else:
            return r.json()

        return

    def login(self, username, password):
        """ Login to nessus and get token """

        login = {'username': username, 'password': password}
        self.token = self.sendRequest('POST', '/session', data=login)['token']

        return

    def logout(self):
        """ Logout of nessus """

        self.sendRequest('DELETE', '/session')

        return

    def getScan(self, scan_id):
        """ Get scan details """

        return(self.sendRequest('GET', '/scans/{0}'.format(scan_id)))

    def getEditorScan(self, scan_id):
        """ Get scan details from editor """

        return(self.sendRequest('GET', '/editor/scan/{0}'.format(scan_id)))

    def addScan(self):
        """ Add a new scan """

        return

    def updateScan(self, scan_id, settings):
        """ Update scan settings """

        if settings:
            return self.sendRequest('PUT', '/scans/{0}'.format(scan_id),
                    data=settings)

    def launchScan(self, scan_id):
        """ Launch a scan """

        data = self.sendRequest('POST', '/scans/{0}/launch'.format(scan_id))

        return data['scan_uuid']

    def deleteScan(self, scan_id):
        """ Delete a scan """

        self.sendRequest('DELETE', '/scans/{0}'.format(scan_id))

        return

    def deleteHistory(self, scan_id, history_id):
        """ Delete a historical scan """

        self.sendRequest('DELETE', '/scans/{0}/history/{1}'.format(scan_id,
            history_id))

        return

    def getScanList(self):
        """ Return the scan list """

        return(self.sendRequest('GET', '/scans'))

    def getPolicyList(self):
        """ Return the policy list """

        return(self.sendRequest('GET', '/policies'))

    def exportScanResult(self, scan_id, report_format, chapters):
        """ Request an export of the results for the specified scan """

        data = {'format': report_format, 'chapters': chapters}

        file_id = self.sendRequest('POST', '/scans/{0}/export'.format(scan_id),
                data=data)

        return file_id

    def exportStatusCheck(self, scan_id, file_id):
        """ Check if the export is ready for download """

        data = self.sendRequest('GET',
                '/scans/{0}/export/{1}/status'.format(scan_id, file_id))

        return data['status'] == 'ready'

    def downloadReport(self, scan_id, file_id, report_format, name, outdir):
        """ Download the scan results stored in the export file """

        data = self.sendRequest('GET',
                '/scans/{0}/export/{1}/download'.format(scan_id, file_id))

        filename = '{0}.{1}'.format(name, report_format)

        with open(os.path.join(outdir, filename), 'w') as f:
            f.write(data.decode('ascii', 'ignore'))

        return

    def getHostDetails(self, scan_id, host_id):
        """ Get details of a scanned host """

        return self.sendRequest('GET', '/scans/{0}/hosts/{1}'.format(scan_id,
            host_id))

    def getPluginOutput(self, scan_id, host_id, plugin_id):
        """ Get plugin output """

        return self.sendRequest('GET',
                '/scans/{0}/hosts/{1}/plugins/{2}'.format(scan_id, host_id,
                    plugin_id))


# EOF
