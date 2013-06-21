from detector import Detector
from saxpy import SAX

import numpy
import string
import operator

class SpikeDetector(Detector):
    ALPHABET_SIZE = 4
    WINDOW_SECONDS_COUNT = 3600 * 8
    SECONDS_PER_SYMBOL = 1200

    @classmethod
    def _get_local_maxima(cls, timeseries):
        """Return all local maxima in timeseries"""
        ret = []
        for i in xrange(1, len(timeseries) - 1):
            left = timeseries[i - 1]
            right = timeseries[i + 1]
            if timeseries[i] > left and timeseries[i] > right:
                ret.append(timeseries[i])

        return ret

    @classmethod
    def _get_basic_spike_prio(cls, value, treshold):
        """Return priority for basic spike that is usually smoothed"""
        prio = (value - treshold) / treshold

        return min(prio, 1.0)

    @classmethod
    def _get_basic_spikes(cls, timeseries, timestamps, treshold):
        """Returns basic spikes that are usually smoothed"""
        return { timestamps[i]:cls._get_basic_spike_prio(timeseries[i], treshold) \
                 for i in range(len(timeseries)) if timeseries[i] > treshold }

    @classmethod
    def _get_SAX_spikes(cls, timeseries, timestamps, treshold):
        """
        Returns spikes counting how many times a timestamp is a maximum
        in a SAX conversion
        """

        # Seconds bethween measurements
        retention = (timestamps[-1] - timestamps[0]) / len(timestamps)

        # Number of entries per window
        entries_per_word = cls.WINDOW_SECONDS_COUNT / retention

        num_windows = len(timeseries) / entries_per_word
        window_size = len(timeseries) / num_windows

        num_symbols = window_size * retention / cls.SECONDS_PER_SYMBOL

        sax_generator = SAX(wordSize = num_symbols, alphabetSize = cls.ALPHABET_SIZE)

        symbols_per_datapoint = int(round(cls.SECONDS_PER_SYMBOL / float(retention)))

        # Convert timeseries into SAX notation
        words, intervals = sax_generator.sliding_window(timeseries, num_windows, .8)

        # Times index i is a maximal value
        maximum_count = {i: 0 for i in xrange(len(timeseries))}
        # Times index i is passed by a window
        window_count = {i: 0 for i in xrange(len(timeseries))}

        # Count in how many windows a timestamp is a local maximum
        for i in xrange(len(words)):
            word = words[i]
            interval = intervals[i]

            for j in xrange(len(word)):
                index = j * symbols_per_datapoint + interval[0]
                if word[j] == string.ascii_lowercase[cls.ALPHABET_SIZE - 1]:
                    maximum_count[index] += 1
                window_count[index] += 1

        spikes = { }
        for key, value in maximum_count.iteritems():
            if value == window_count[key] and value and \
               timeseries[key] > treshold:
                   val = timeseries[key]
                   spikes[timestamps[key]] = cls._get_basic_spike_prio(val, treshold)

        return spikes

    @classmethod
    def _get_top_spikes(cls, spikes, duration):
        """Returns top spikes having tiestamps that differ by duration"""
        ret = []

        while len(spikes):
            # Get the spike with the maximum priority
            max_ts = max(spikes.iteritems(), key=operator.itemgetter(1))[0]

            if spikes[max_ts] > .2:
                ret.append((max_ts, spikes[max_ts]))

            spikes = { k: v for k, v in spikes.iteritems() \
                       if abs(k - max_ts) > duration }

        return ret

    @classmethod
    def detect_anomalies(cls, timeseries, timestamps):
        """Detects anomalies in a timeseries"""

        try:
            super(cls, SpikeDetector).detect_anomalies(timeseries, timestamps)
        except ValueError:
            return []

        # Check empty lists
        if len(timeseries) == 0:
            return []

        # Get the mean of all local maxima to have a treshold for spikes
        max_value = numpy.mean(cls._get_local_maxima(timeseries))

        # Save a copy of original timeseries
        orig_timeseries = timeseries[:]

        # Smoooth data
        cls.smooth_data(timeseries, 2)

        # Get maxima in unsmoothed timeseries
        basic_spikes = cls._get_basic_spikes(orig_timeseries, timestamps, 5 * max_value)

        # Get spikes using SAX conversion in the smoothed timeseries
        SAX_spikes = cls._get_SAX_spikes(timeseries, timestamps, max_value)

        #create merged dict
        spikes = dict(basic_spikes, **SAX_spikes)

        return cls._get_top_spikes(spikes, cls.WINDOW_SECONDS_COUNT)

