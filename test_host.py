#!/usr/bin/env python

import json
import os
import re
import requests
import sys
import time

USAGE = "test_host host_string target_pattern"
SLEEP_VAL = 1

def main(host_string, pattern):
    response = requests.get("http://%s/metrics/index.json" % host_string)

    targets = json.loads(response.text)

    targets = [t for t in targets if re.match(pattern, t) is not None]

    for target in targets:
        os.system("./test_metric.py %s %s" % (host_string, target))
        time.sleep(SLEEP_VAL)

if __name__ == "__main__":
    if len(sys.argv) is not 3:
        print USAGE
        sys.exit(-1)
    sys.exit(main(*sys.argv[1:]))

