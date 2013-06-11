class Detector(object):
    """Base class for detecting errors in timeseries"""
    def __init__(self):
        pass

    def detect_anomalies(self, timeseries, retention, starting_time = 0):
        """Detects anomalies in a timeseries"""
        pass
