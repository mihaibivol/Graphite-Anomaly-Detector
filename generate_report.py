#!/usr/bin/env python

import csv
import fnmatch
import json
import requests
import time
import sys

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from detector import SpikeDetector

DESCRIPTION = "Generates CSV report with spikes found on Graphite hosts"

# Sleep value bethween requests to same host
DEFAULT_SLEEP_VAL = 1
# Limit of requests per host
DEFAULT_HOST_LIMIT = 500
# Output file
DEFAULT_OUTPUT_FILE = None

# Detector class
DETECTOR = SpikeDetector()

def get_host_targets(host_string, pattern):
    """Returns targets that match pattern from a graphite host"""
    response = requests.get('http://%s/metrics/index.json' % host_string)

    targets = json.loads(response.text)

    targets = [t for t in targets if fnmatch.fnmatch(t, pattern)]

    return targets

def get_timeseries(host_string, target):
    """Returns tuple timeseries, timestamps for host"""
    url = 'http://%s/render/' % host_string
    payload = {
            'target': target,
            'format': 'json' }
    response = requests.get(url, params = payload)

    data = json.loads(response.text)

    detector_data = data[0]['datapoints']

    timeseries = [t[0] for t in detector_data]
    timestamps = [t[1] for t in detector_data]

    return timeseries, timestamps

def process(targets, timeout, output_file):
    # Send requests without timeouts to all servers
    results = []

    while len(targets) != 0:
        for host_string in targets.keys():
            # Get target
            target = targets[host_string].pop()
            # Check remaining targets
            if len(targets[host_string]) == 0:
                del targets[host_string]

            # Process
            timeseries, timestamps = get_timeseries(host_string, target)
            try:
                anomalies = DETECTOR.detect_anomalies(timeseries, timestamps)
            except Exception:
                print "Exception occured during detect_anomalies"

            for timestamp, priority in anomalies:
                data = [host_string, target, time.ctime(timestamp), priority]
                results.append(data)

        # Sleep bethween requests
        time.sleep(timeout)

    if output_file is None:
        return

    # Write results to csv file
    with open(output_file, 'w') as f:
        csv_writer = csv.writer(f, delimiter = ' ')
        csv_writer.writerows(results)

def get_arguments():
    arg_parser = ArgumentParser(description = DESCRIPTION,
                                formatter_class = ArgumentDefaultsHelpFormatter)

    arg_parser.add_argument('-s', '--servers',
                            nargs = '+',
                            required = True,
                            help = 'Servers queried by program')

    arg_parser.add_argument('-l', '--limit',
                            nargs = 1,
                            default = [DEFAULT_HOST_LIMIT],
                            type = int,
                            help = 'Limit request count per host')

    arg_parser.add_argument('-p', '--pattern',
                            nargs = 1,
                            default = ['*'],
                            type = str,
                            help = 'Glob pattern for metrics')

    arg_parser.add_argument('-t', '--timeout',
                            nargs = 1,
                            default = [DEFAULT_SLEEP_VAL],
                            type = int,
                            help = 'Timeout bethween requests for host')

    arg_parser.add_argument('-o', '--output',
                            nargs = 1,
                            default = [DEFAULT_OUTPUT_FILE],
                            type = str,
                            help = 'Output CSV file')

    arg_parser.add_argument('-u', '--upload',
                            action = 'store_true',
                            help = 'Upload to Google Drive using config.py')

    return arg_parser.parse_args(sys.argv[1:])

def main():
    args = vars(get_arguments())

    pattern = args['pattern'][0]
    limit = args['limit'][0]
    timeout = args['timeout'][0]
    output_file = args['output'][0]

    # Get servers targets
    targets = { s: get_host_targets(s, pattern)[:limit] \
                for s in args['servers'] }

    process(targets, timeout, output_file)

if __name__ == "__main__":
    sys.exit(main())
