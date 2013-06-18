#!/usr/bin/env python

import json
import os
import requests
import sys
import time

USAGE = "test_host host_string"
SLEEP_VAL = 1

def main(host_string):
    response = requests.get("http://%s/metrics/index.json" % host_string)

    targets = json.loads(response.text)

    for target in targets:
        os.system("./test_metric.py %s %s" % (host_string, target))
        time.sleep(SLEEP_VAL)

if __name__ == "__main__":
    if len(sys.argv) is not 2:
        print USAGE
        sys.exit(-1)
    sys.exit(main(sys.argv[1]))

