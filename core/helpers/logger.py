# -*- coding:utf-8 -*-
# @module logger
# @since 2020.02.23, 02:18
# @changed 2023.02.09, 18:06

import math
from os import path
import datetime
import yaml
#  from termcolor import colored

from django.conf import settings

from core.constants import logging_options
from core.constants import date_time_formats

from . import yamlSupport


def getDateStr(now=None, isDetailed=False):
    if now is None or not now:
        now = datetime.datetime.now()  # Get current date object
    formatStr = date_time_formats.detailedDateFormat if isDetailed else date_time_formats.preciseDateFormat
    dateTag = now.strftime(formatStr)
    return dateTag


def getMsDateTag(now=None, isDetailed=False):
    if now is None or not now:
        now = datetime.datetime.now()  # Get current date object
    # Format date like '2022.02.08-02:04:23.255157' or '220208-020423-255157'
    # (Only formats with milliseconds, see next command)
    formatStr = date_time_formats.detailedDateFormat if isDetailed else date_time_formats.logDateFormat
    dateTag = now.strftime(formatStr)
    dateTag = dateTag[:-3]  # Convert microseconds (.NNNNNN) to milliseconds (.NNN)
    return dateTag


def getMsTimeStamp(now=None):
    if now is None or not now:
        now = datetime.datetime.now()  # Get current date object
    timestamp = math.floor(now.timestamp() * 1000)  # Get milliseconds timestamp (for technical usage)
    return timestamp


def createHeader():
    now = datetime.datetime.now()  # Get current date object
    timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
    dateTag = getMsDateTag(now, True)
    header = '[' + str(timestamp) + ' ' + dateTag + ']'
    return header


def createLogData(_title, data=None):
    logData = ''
    if data is not None:
        logData = yaml.dump(data,
                            Dumper=yamlSupport.CustomYamlDumper,
                            #  encoding='utf-8',  # Produces binary (`b'`) string
                            #  encoding=None,  # Produces unicode string
                            allow_unicode=True,
                            default_flow_style=False,
                            indent=2)
        logData = logData.replace('!!python/unicode ', '')
        logData = '  ' + logData.replace('\n', '\n  ').rstrip()  # Indent data
        if not logData.endswith('\n'):
            logData += '\n'
        #  if 'test' in data:
        #      print('Test data:', data)
        #      print('Test yaml:', logData)
    return logData


hasLoggedEntries = False


def DEBUG(title, data=None):
    global hasLoggedEntries  # pylint: disable=global-statement
    header = createHeader()
    logData = createLogData(title, data)  # Ensure trailing newline for record delimiting
    fileMode = 'ab'  # Default file mode: append (ab)
    if not hasLoggedEntries:
        #  print('[Log started]\n'  # Insert empty line to stdout)
        if logging_options.clearLogFile:
            fileMode = 'wb'  # Clear file on first entry (wb)
        hasLoggedEntries = True
    if logging_options.writeLog:
        rootPath = settings.ROOT_PATH
        logFile = path.join(rootPath, logging_options.logFileName)
        #  with open(logFile, fileMode, encoding='utf-8') as file:
        with open(logFile, fileMode) as file:
            file.write((header + '\n' + title + '\n' + logData + '\n').encode('utf-8'))
    if logging_options.outputLog:
        #  # NOTE: This code breaks server execution too
        #  if logging_options.outputColoredLog:
        #      header = colored(header, 'green')
        #      title = colored(title, 'red')
        print(header + "\n" + title + "\n" + logData)
        #  print(header)
        #  print(title)
        #  print(logData)


__all__ = [  # Exporting objects...
    'DEBUG',
]

if __name__ == '__main__':  # Test
    DEBUG('Test')
