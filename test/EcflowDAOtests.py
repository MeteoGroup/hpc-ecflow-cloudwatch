from EcflowDAO import EcflowDAO
import unittest

from ecflow_metrics import EcflowMetrics
from ecflow_state_parser import EcflowStateParser
from metric_aggregator import MetricAgregator
from metric_converter import MetricsConverters
import json


class TestEcflowDAO(unittest.TestCase):

    def testEcflowParser(self):
        ecflow_metrics = EcflowMetrics()
        prometheus_metrics = ecflow_metrics.get_ecflow_metrics()
        print(prometheus_metrics)


