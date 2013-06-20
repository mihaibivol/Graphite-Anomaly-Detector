Graphite-Anomaly-Detector
=========================

Command line application that determines spikes in Graphite metrics for a given host and generates a CSV report

Usage
-----
<pre>
usage: generate_report.py [-h] -s SERVERS [SERVERS ...] -o OUTPUT [-l LIMIT]
                          [-p PATTERN] [-t TIMEOUT]

Generates CSV report with spikes found on Graphite hosts

optional arguments:
  -h, --help            show this help message and exit
  -s SERVERS [SERVERS ...], --servers SERVERS [SERVERS ...]
                        Servers queried by program (default: None)
  -o OUTPUT, --output OUTPUT
                        Output CSV file (default: [None])
  -l LIMIT, --limit LIMIT
                        Limit request count per host (default: [500])
  -p PATTERN, --pattern PATTERN
                        Glob pattern for metrics (default: ['*'])
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout bethween requests for host (default: [1])
</pre>

For example
<pre>
./generate_report.py -s dumdum:81 -o report.csv -l 2 -p *.cpu.* -t 42
</pre>

Will gather the first two metrics that match \*.cpu.\* with 42 seconds timeout bethween the requests.
The command will ouptut the results in report.csv

Result
------

The program creates a csv file ginven as argument for the --output option having 5 columns:

HOST, METRIC, TIME, RELEVANCE, GRAPH_URL

Developing Detectors
--------------------
TODO

Testing Detectors
-----------------

For testing you can use test_local.py.

It requires matplotlib for plotting the results.

test_local.py receives a Graphite json response for a given target and plots the following:
 * Original timeseries
 * Timeseries after running the detector
 * Detector results
 * A treshold line (you can remove it while testing)

You just have to replace SpikeDetector with your detector.
