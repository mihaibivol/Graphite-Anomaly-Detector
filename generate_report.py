#!/usr/bin/env python

import fnmatch
import json
import requests
import time
import sys

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

DESCRIPTION = "Generates CSV report with spikes found on Graphite hosts"

# Sleep value bethween requests to same host
SLEEP_VAL = 1
# Limit of requests per host
HOST_LIMIT = 500
# Output file
OUTPUT_FILE = 'report.csv'

def get_host_targets(host_string, pattern):
    """Returns targets that match pattern from a graphite host"""
    pass

def get_timeseries(host_string, target):
    """Returns target timeseries for host"""
    pass

def detect_anomalies(detector, timestamps, timeseries):
    """Returns spikes found in timeseries using detector"""
    pass

def process_host(host_string, target):
    """Returns spikes found target timeseries for host"""
    pass

def get_arguments():
    arg_parser = ArgumentParser(description = DESCRIPTION,
                                formatter_class = ArgumentDefaultsHelpFormatter)

    arg_parser.add_argument('-s', '--servers',
                            nargs = '+',
                            required = True,
                            help = 'Servers queried by program')

    arg_parser.add_argument('-l', '--limit',
                            nargs = 1,
                            default = [HOST_LIMIT],
                            type = int,
                            help = 'Limit request count per host')

    arg_parser.add_argument('-p', '--pattern',
                            nargs = 1,
                            default = ['*'],
                            type = str,
                            help = 'Glob pattern for metrics')

    arg_parser.add_argument('-t', '--timeout',
                            nargs = 1,
                            default = [HOST_LIMIT],
                            type = int,
                            help = 'Timeout bethween requests for host')

    arg_parser.add_argument('-o', '--output',
                            nargs = 1,
                            default = [OUTPUT_FILE],
                            type = str,
                            help = 'Output CSV file')

    arg_parser.add_argument('-u', '--upload',
                            action = 'store_true',
                            help = 'Upload to Google Drive using config.py')

    return arg_parser.parse_args(sys.argv[1:])

def main():
    args = get_arguments()
    print args

if __name__ == "__main__":
    sys.exit(main())
