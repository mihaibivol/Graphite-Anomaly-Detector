#!/usr/bin/env python

from util.logger import view_logfile
from pylab import show

import sys

def main(logfiles):
    for logfile in logfiles:
        view_logfile(logfile, False)
    show()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

