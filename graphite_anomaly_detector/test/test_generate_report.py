from graphite_anomaly_detector.generate_report import process_targets, process
from unittest import TestCase

import mock

class CSVWriterMock(object):
    """Mocks a csv writer that writes into a list rather than a file"""
    def __init__(self):
        self.lines = []

    def writerow(self, data):
        self.lines.append(data)

class DetectorMock(object):
    """Produces two anomalies for any givem timeseries"""
    def detect_anomalies(self, timeseries, timestamp):
        return [(1, .1), (2, .2)]

class TestGenerateReport(TestCase):
    def setUp(self):
        pass

    @mock.patch('graphite_anomaly_detector.generate_report.get_timeseries', lambda x, y : ([1, 2, 3], [4, 5, 6]))
    def test_processing(self):
        """Test that all targets are processed"""

        s1 = 'gigi'
        s2 = 'marean'

        t1 = ['becali', 'meme']
        t2 = ['vanghelie']

        expected_results = 2 * (len(t1) + len(t2))

        # Test servers with a list of metrics
        targets = {s1: t1, s2: t2}

        writer = CSVWriterMock()
        detector = DetectorMock()

        process_targets(targets, 0, writer, detector)

        lines = writer.lines
        # Test all metrics produced two spikes
        self.assertEqual(len(lines), expected_results,
                         "Not all targets were processed")

    def test_process_with_no_file(self):
        """Test that process with None raises Exception"""

        self.assertRaises(AssertionError,
                          process,
                          None, None, None, None)
