class Detector(object):
    """Base class for detecting errors in timeseries"""
    def __init__(self):
        pass

    @classmethod
    def detect_anomalies(cls, timeseries, timestamps):
        """Detects anomalies in a timeseries"""
        assert len(timeseries) == len(timestamps), \
               "Must provide equal length timeseries and timestamp lists"

        # Check many None values
        if timeseries.count(None) > len(timeseries) / 2:
            raise ValueError("Can't generate anomalies with too many None values")

        # Convert null values
        cls.convert_null_values(timeseries)

    @classmethod
    def convert_null_values(cls, timeseries):
        for i in xrange(len(timeseries)):
            timeseries[i] = 0 if timeseries[i] is None else timeseries[i]

    @classmethod
    def smooth_data(cls, timeseries, level = 3):
        """
        Smooth local maxima and minima level times.

        Smoothing is done by eliminating local maxima and minima and
        replacing them with the mean of the neighbours
        """
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

