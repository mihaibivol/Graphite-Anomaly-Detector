from detector import Detector
from saxpy import SAX

import numpy
import string

class SpikeDetector(Detector):
    ALPHABET_SIZE = 4
    WINDOW_SECONDS_COUNT = 3600 * 12
    SECONDS_PER_SYMBOL = 1200

    TRESHOLD_FACTOR = .1

    @classmethod
    def detect_anomalies(cls, timeseries, timestamps):
        """Detects anomalies in a timeseries"""
        super(cls, SpikeDetector).detect_anomalies(timeseries, timestamps)

        # Get maximum before smoothing
        max_value = max(timeseries)

        # Smoooth data
        cls.smooth_data(timeseries)

        # Seconds bethween measurements
        retention = (timestamps[-1] - timestamps[0]) / len(timestamps)

        # Number of entries per window
        entries_per_word = cls.WINDOW_SECONDS_COUNT / retention

        num_windows = len(timeseries) / entries_per_word
        window_size = len(timeseries) / num_windows

        num_symbols = window_size * retention / cls.SECONDS_PER_SYMBOL

        sax_generator = SAX(wordSize = num_symbols, alphabetSize = cls.ALPHABET_SIZE)

        # TODO really ugly aproximation
        symbols_per_datapoint = int(round(cls.SECONDS_PER_SYMBOL / float(retention)))

        # Convert timeseries into SAX notation
        words, intervals = sax_generator.sliding_window(timeseries, num_windows, .9)

        # Times index i is a maximal value
        maximum_count = {i: 0 for i in xrange(len(timeseries))}
        # Times index i is passed by a window
        window_count = {i: 0 for i in xrange(len(timeseries))}

        for i in xrange(len(words)):
            word = words[i]
            interval = intervals[i]

            for j in xrange(len(word)):
                index = j * symbols_per_datapoint + interval[0]
                if word[j] == string.ascii_lowercase[cls.ALPHABET_SIZE - 1]:
                    maximum_count[index] += 1
                window_count[index] += 1

        treshold = cls.TRESHOLD_FACTOR * max_value

        for key, value in maximum_count.iteritems():
            if value == window_count[key] and value and \
               timeseries[key] > treshold:
                yield timestamps[key]


