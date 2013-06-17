from saxpy import SAX

import string

class Detector(object):
    """Base class for detecting errors in timeseries"""
    def __init__(self):
        pass

    @classmethod
    def detect_anomalies(cls, timeseries_data):
        """Detects anomalies in a timeseries"""
        pass

    @classmethod
    def smooth_data(cls, timeseries_data, level = 3):
        """Smooth local maxima level times"""
        while level:
            cls._smooth_data(timeseries_data)
            level -= 1


    @classmethod
    def _smooth_data(cls, timeseries_data):
        """Smooth local maxima"""

        #TODO change format to be independent from Graphite
        for i in xrange(1, len(timeseries_data['datapoints']) - 1):
            left = timeseries_data['datapoints'][i - 1][0]
            right = timeseries_data['datapoints'][i + 1][0]
            if left > timeseries_data['datapoints'][i][0] and \
               right > timeseries_data['datapoints'][i][0]:
                timeseries_data['datapoints'][i][0] = (left + right) / 2


class TimeSeriesBitmap2D(object):
    def __init__(self, alphabet, string=""):
        self._bitmap = {}
        self._keys = set()
        self.alphabet = alphabet

        #init bitmap
        for l1 in alphabet:
            for l2 in alphabet:
                self._keys.add(l1 + l2)
                self._bitmap[l1 + l2] = 0

        # Add occurrences from string
        for i in xrange(len(string) - 1):
            self.add_occurrence(string[i] + string[i + 1])

    def __add__(self, other):
        result = TimeSeriesBitmap2D(self.alphabet)

        for key in self._keys:
            result._bitmap[key] = self._bitmap[key] + other._bitmap[key]

        return result

    def add_occurrence(self, string):
        assert len(string) == 2, "You can only add a occurrence of 2 letters in a bitmap"
        assert string in self._keys, "Invalid charset"

        self._bitmap[string] += 1

    def distance(self, other):
        res = 0

        max_self = max(self._bitmap.values())
        max_other = max(other._bitmap.values())

        for key in self._keys:
            res += (float(self._bitmap[key]) / max_self -
                    float(other._bitmap[key]) / max_other) ** 2
        return res / len(self._keys)

class SpikeDetector(Detector):
    ALPHABET_SIZE = 4
    WINDOW_SECONDS_COUNT = 3600 * 12
    SECONDS_PER_SYMBOL = 1200

    @classmethod
    def detect_anomalies(cls, timeseries_data):
        """Detects anomalies in a timeseries"""

        cls.smooth_data(timeseries_data)

        timeseries = [d[0] for d in timeseries_data['datapoints']]
        timestamps = [d[1] for d in timeseries_data['datapoints']]

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
        words, intervals = sax_generator.sliding_window(timeseries, num_windows, .8)

        maximum_count = {i: 0 for i in xrange(len(timeseries))}

        for i in xrange(len(words)):
            word = words[i]
            interval = intervals[i]

            for j in xrange(len(word)):
                index = j * symbols_per_datapoint + interval[0]
                if word[j] == string.ascii_lowercase[cls.ALPHABET_SIZE - 1]:
                    maximum_count[index] += 1

        max_value = max(maximum_count.values())

        for key, value in maximum_count.iteritems():
            if value == max_value:
                yield (0, (0, timestamps[key]))

class SlidingWindowDetector(Detector):
    WORD_SIZE = 4
    ALPHABET_SIZE = 4

    WINDOW_WORD_COUNT = 3
    WINDOW_SECONDS_COUNT = 3600

    @classmethod
    def detect_anomalies(cls, timeseries_data):
        """Detects anomalies in a timeseries"""

        timeseries = [d[0] for d in timeseries_data['datapoints']]
        timestamps = [d[1] for d in timeseries_data['datapoints']]

        # Seconds bethween measurements
        retention = (timestamps[-1] - timestamps[0]) / len(timestamps)

        # Number of entries per window
        entries_per_word = cls.WINDOW_SECONDS_COUNT / retention / cls.WINDOW_WORD_COUNT

        num_windows = len(timeseries) / entries_per_word

        sax_generator = SAX(wordSize = cls.WORD_SIZE, alphabetSize = cls.ALPHABET_SIZE)

        alphabet = [string.ascii_lowercase[i] for i in range(cls.ALPHABET_SIZE)]

        # Convert timeseries into SAX notation
        words, intervals = sax_generator.sliding_window(timeseries, num_windows, .5)

        overlap_offset = (intervals[0][1] - intervals[0][0]) / intervals[1][0]

        for i in xrange(len(words) - overlap_offset * cls.WINDOW_WORD_COUNT * 2):
            # Calculate distance bethween two concatenated windows lead and lag.
            lag_window = []
            lag_intervals = []
            lead_window = []
            lead_intervals = []

            window_offset = overlap_offset * cls.WINDOW_WORD_COUNT
            for j in xrange(i, i + window_offset, overlap_offset):
                lag_window.append(words[j])
                lag_intervals.append(intervals[j])

            for j in xrange(i + window_offset, i + 2 * window_offset, overlap_offset):
                lead_window.append(words[j])
                lead_intervals.append(intervals[j])

            lag_bitmap = TimeSeriesBitmap2D(alphabet)
            lead_bitmap = TimeSeriesBitmap2D(alphabet)

            for w in lag_window:
                lag_bitmap += TimeSeriesBitmap2D(alphabet, w)

            for w in lead_window:
                lead_bitmap += TimeSeriesBitmap2D(alphabet, w)

            distance = lag_bitmap.distance(lead_bitmap)

            if distance > .5:
                yield (distance, (timestamps[lag_intervals[0][0]], timestamps[lead_intervals[-1][1]]))
