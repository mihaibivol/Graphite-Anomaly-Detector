#!/usr/bin/env python

from util.logger import view_logfile

import sys

USAGE = "view_log logfile"

def main(logfile):
    view_logfile(logfile)

if __name__ == "__main__":
    if len(sys.argv) is not 2:
        print USAGE
        sys.exit(-1)
    sys.exit(main(sys.argv[1]))

