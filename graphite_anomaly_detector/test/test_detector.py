from graphite_anomaly_detector.detector.detector import Detector
from unittest import TestCase

class TestDetector(TestCase):

    def setUp(self):
        self.detector = Detector()

    def test_detect_anomalies_params(self):
        """Test that detect_anomalies raises errors with bad parameters"""
        self.assertRaises(AssertionError,
                          self.detector.detect_anomalies,
                          [1, 2], [1])

    def test_sparse_timeseries(self):
        """Test that sparse timeseries raise ValueError"""
        timeseries = [1, None, None, None, None, 2]
        timestamps = range(len(timeseries))

        self.assertRaises(ValueError,
                          self.detector.detect_anomalies,
                          timeseries, timestamps)

    def test_convert_null_values(self):
        """Test that None values are converted to 0"""
        timeseries = [1, None, 2, None, 3, 4]
        self.detector.convert_null_values(timeseries)

        self.assertFalse(None in timeseries,
                         "None values aren't converted to 0")

    def test_smooth_data(self):
        """Test that local maxima and minima are smoothed"""
        timeseries = [1, 2, 1]
        self.detector.smooth_data(timeseries)

        self.assertEqual(timeseries[1], 1,
                         "Local max is not smoothed")

        timeseries = [1, -1, 1]
        self.detector.smooth_data(timeseries)

        self.assertEqual(timeseries[1], 1,
                         "Local min is not smoothed")


