class Detector(object):
    """Base class for detecting errors in timeseries"""
    def __init__(self):
        pass

    @classmethod
    def detect_anomalies(cls, timeseries, timestamps):
        """Detects anomalies in a timeseries"""
        assert len(timeseries) == len(timestamps), \
               "Must provide equal length timeseries and timestamp lists"

    @classmethod
    def smooth_data(cls, timeseries, level = 3):
        """Smooth local maxima and minima level times"""
        while level:
            cls._smooth_data(timeseries)
            level -= 1


    @classmethod
    def _smooth_data(cls, timeseries):
        """Smooth local maxima and minima"""
        for i in xrange(1, len(timeseries) - 1):
            left = timeseries[i - 1]
            right = timeseries[i + 1]
            if left < timeseries[i] and right < timeseries[i]:
                timeseries[i] = (left + right) / 2

            if left > timeseries[i] and right > timeseries[i]:
                timeseries[i] = (left + right) / 2

