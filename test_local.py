#!/usr/bin/env python

from detector import SpikeDetector
from util.plot import plot_data

import sys
import json

DETECTOR = SpikeDetector()

def main(filename):
    fp = open(filename, 'r')

    data = json.load(fp)

    fp.close()

    detector_data = data[0]['datapoints']

    timeseries = [t[0] for t in detector_data]
    SpikeDetector.convert_null_values(timeseries)
    timestamps = [t[1] for t in detector_data]

    orig_series = timeseries[:]
    orig_stamps = timestamps[:]

    res = DETECTOR.detect_anomalies(timeseries, timestamps)

    plot_data(filename, (orig_stamps, orig_series), (timestamps, timeseries), res)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

