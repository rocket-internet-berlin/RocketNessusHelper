# Nessus-helper

A Nessus helper. https://www.rocket-internet.com/

## Overview

Tenable Nessus offers an API to manage your scans. It allows you to export and
download reports and more.

This tool provides options to export and download nessus scans and
optionally send them via email to mailing lists of your choice.

More options will be defined in the near future

## Nessus setup

You must set up a Nessus user account in order to use this tool. The account
role (e.g. permissions) is irrelevant.

## Nessus-Helper setup

This tool has only few dependencies. To install all of the dependencies run:
```
pip -r requirements.txt
```
and run:
```
./src/nessus-helper -H
```
