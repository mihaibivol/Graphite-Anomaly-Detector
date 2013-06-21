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

    targets = []
    try:
        response = requests.get('http://%s/metrics/index.json' % host_string)

        targets = json.loads(response.text)

        targets = [t for t in targets if fnmatch.fnmatch(t, pattern)]
    except Exception as e:
        print 'Exception occured while getting host target: %s' % e
    finally:
        return targets

def get_anomaly_url(host_string, target, timestamp):
    url_base = '=HYPERLINK(\"http://%s/render/?target=%s&from=%s&until=%s&width=1200&height=600\")'

    half_day = 12 * 3600
    return url_base % (host_string, target,
                       timestamp - half_day, timestamp + half_day)

def get_timeseries(host_string, target):
    """Returns tuple timeseries, timestamps for host matching target"""

    url = 'http://%s/render/' % host_string
    payload = {
            'target': target,
            'format': 'json' }

    timeseries = []
    timestamps = []
    try:
        response = requests.get(url, params = payload)

        data = json.loads(response.text)

        detector_data = data[0]['datapoints']

        timeseries = [t[0] for t in detector_data]
        timestamps = [t[1] for t in detector_data]
    except Exception as e:
        print 'Exception occured while getting timeseries' \
              'for %s with target %s: %s' % (host_string, target, e)

    finally:
        return timeseries, timestamps

def process(targets, timeout, output_file, detector):
    """Process the received targets and output to output_file"""
    assert output_file is not None, \
          'Must give a valid output file'

    with open(output_file, 'w') as f:
        csv_writer = csv.writer(f, delimiter = ' ')
        process_targets(targets, timeout, csv_writer, detector)

def process_targets(targets, timeout, csv_writer, detector):
    """Process the received targets and output to csv_writer"""

    # Send requests without timeouts to all servers
    while len(targets) != 0:
        for host_string in targets.keys():
            # Check remaining targets
            if len(targets[host_string]) == 0:
                del targets[host_string]
                continue

            # Get target
            target = targets[host_string].pop()

            # Process
            timeseries, timestamps = get_timeseries(host_string, target)
            try:
                anomalies = detector.detect_anomalies(timeseries, timestamps)
            except Exception:
                print 'Exception occured during detect_anomalies: %s' % e

            for timestamp, priority in anomalies:
                data = [host_string, target, time.ctime(timestamp), priority,
                        get_anomaly_url(host_string, target, timestamp)]
                csv_writer.writerow(data)

        # Sleep bethween requests
        time.sleep(timeout)
        print 'Processed %s' % target

def get_arguments():
    arg_parser = ArgumentParser(description = DESCRIPTION,
                                formatter_class = ArgumentDefaultsHelpFormatter)

    arg_parser.add_argument('-s', '--servers',
                            nargs = '+',
                            required = True,
                            help = 'Servers queried by program')

    arg_parser.add_argument('-o', '--output',
                            nargs = 1,
                            default = [DEFAULT_OUTPUT_FILE],
                            required = True,
                            type = str,
                            help = 'Output CSV file')

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

    process(targets, timeout, output_file, DETECTOR)

if __name__ == "__main__":
    sys.exit(main())
