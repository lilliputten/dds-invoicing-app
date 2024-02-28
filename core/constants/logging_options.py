# Logging...

from django.conf import settings


outputLog = True  # Print log to stdout
outputColoredLog = settings.LOCAL  # Use rich output log format with `termcolor` (don't use for server; it can break apache logging)
writeLog = True  # Write log to external file
clearLogFile = True  # Clear log file at start
logFileName = 'log.txt'  # Log file name (relative to `rootPath`!)


__all__ = [  # Exporting objects...
    'outputLog',
    'outputColoredLog',
    'writeLog',
    'clearLogFile',
    'logFileName',
]
