#!/usr/bin/env python

from detector.detector import SlidingWindowDetector, SpikeDetector
from pylab import show, plot

import sys
import json
import time

def main(filename):
    fp = open(filename, 'r')

    data = json.load(fp)

    fp.close()

    res = SpikeDetector.detect_anomalies(data[0])
    plot_data(data[0], res)
    for r in res:
        print r[0], time.ctime(r[1][0]), time.ctime(r[1][1])

def plot_data(data, res):
    timeseries = [d[0] for d in data['datapoints']]
    timestamps = [d[1] for d in data['datapoints']]

    r_t, r_d = [], []
    for r in res:
        r_t.append(r[1][1])
        r_d.append(0)

    plot(timestamps, timeseries, r_t, r_d, "rs")
    show()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

