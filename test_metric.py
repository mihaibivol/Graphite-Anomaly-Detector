#!/usr/bin/env python

from detector import SpikeDetector
from util.logger import create_logfile, view_logfile

import sys
import json
import requests

USAGE = "test_metric host_string target [start end]"

HOUR_COUNT = [4, 8, 12]
SECONDS_PER_SYMBOL = [600, 1200]

TEST_CASES = [(h, s) for h in HOUR_COUNT for s in SECONDS_PER_SYMBOL]

def test_case(window_hour_count, seconds_per_symbol,
              timeseries, timestamps, name):
    SpikeDetector.WINDOW_SECONDS_COUNT = window_hour_count * 3600
    SpikeDetector.SECONDS_PER_SYMBOL = seconds_per_symbol

    timeseries_c = timeseries[:]
    timestamps_c = timestamps[:]

    res = SpikeDetector.detect_anomalies(timeseries_c, timestamps_c)

    create_logfile("log/%d_%d_%s.log" % (window_hour_count, seconds_per_symbol,
                                         name),
                   (timestamps, timeseries),
                   (timestamps_c, timeseries_c), res)



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

    if sum(timeseries) == 0:
        return

    timestamps = [t[1] for t in detector_data]

    for h, s in TEST_CASES:
        test_case(h, s, timeseries, timestamps, "%s_%s" % (host_string, target))


if __name__ == "__main__":
    if len(sys.argv) is not 3 and len(sys.argv) is not 5:
        print USAGE
        sys.exit(-1)
    sys.exit(main(*sys.argv[1:]))

