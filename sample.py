#!/usr/bin/env python

from detector import SlidingWindowDetector, SpikeDetector
from util.plot import plot_data

import sys
import json

def main(filename):
    fp = open(filename, 'r')

    data = json.load(fp)

    fp.close()

    detector_data = data[0]['datapoints']

    timeseries = [t[0] for t in detector_data]
    timestamps = [t[1] for t in detector_data]

    orig_series = timeseries[:]
    orig_stamps = timestamps[:]

    res = SpikeDetector.detect_anomalies(timeseries, timestamps)

    plot_data((orig_stamps, orig_series), (timestamps, timeseries), res)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

