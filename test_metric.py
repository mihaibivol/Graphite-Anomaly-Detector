#!/usr/bin/env python

from detector import SpikeDetector
from util.logger import create_logfile, view_logfile

import sys
import json
import requests

USAGE = "test_metric host_string target [start end]"

def main(host_string, target, start = None, end = None):
    payload = {
            'target': target,
            'from': start,
            'until': end,
            'format': 'json' }

    if start is None:
        payload.pop('from')

    if end is None:
        payload.pop('until')

    response = requests.get("http://%s/render/" % host_string, params = payload)

    data = json.loads(response.text)

    detector_data = data[0]['datapoints']

    timeseries = [t[0] for t in detector_data]
    SpikeDetector.convert_null_values(timeseries)
    timestamps = [t[1] for t in detector_data]

    orig_series = timeseries[:]
    orig_stamps = timestamps[:]

    res = SpikeDetector.detect_anomalies(timeseries, timestamps)

    create_logfile("gigi", (orig_stamps, orig_series), (timestamps, timeseries), res)

if __name__ == "__main__":
    if len(sys.argv) is not 3 and len(sys.argv) is not 5:
        print USAGE
        sys.exit(-1)
    sys.exit(main(*sys.argv[1:]))

