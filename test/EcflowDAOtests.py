from ecflow_cloudwatch.EcflowDAO import EcflowDAO
import unittest

from ecflow_cloudwatch.ecflow_metrics import get_ecflow_metrics
from ecflow_cloudwatch.ecflow_state_parser import EcflowStateParser
from ecflow_cloudwatch.metric_aggregator import MetricAgregator
from ecflow_cloudwatch.metric_converter import MetricsConverters
import json


class TestEcflowDAO(unittest.TestCase):

    def testEcflowParser(self):
        ecflow_metrics = get_ecflow_metrics()
        print(ecflow_metrics)


