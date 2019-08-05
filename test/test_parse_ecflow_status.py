import unittest
import jsonschema
import logging
import os

from ecflow_cloudwatch.ecflow_state_parser import EcflowStateParser
from ecflow_cloudwatch.metric_aggregator import MetricAgregator
import json

import ecflow



class TestParseEcflowStats(unittest.TestCase):

    def setUp(self):
        parser = EcflowStateParser(self.get_test_data())
        self.metrics = parser.parse()
        self.aggregator = MetricAgregator(self.metrics)

    def get_test_data(self):
        cwd = os.getcwd()
        ecflow_states_test_data_sets = "{}/data/ecflow_sample_state".format(cwd)
        return ecflow.Defs(ecflow_states_test_data_sets)

    def testPrepareCloudwatchMetrics(self):
        counts = self.aggregator.get_counts()
        self.assertTrue(len(counts)>0)

    def testEcflowParser(self):
        print(json.dumps(self.metrics, indent=4))
        self.assertTrue(len(self.metrics)>0)

    def testAggregatorCount(self):
        counts = self.aggregator.get_counts()
        print json.dumps(counts, indent=4)
        with open("{}/data/counts.json".format(os.getcwd())) as cjs:
            schema_data = cjs.read()
        schema = json.loads(schema_data)
        jsonschema.validate(counts, schema)

    def testGetMeters(self):
        output = self.aggregator.get_metrics_meters()
        self.assertTrue(len(output)>0)
        #print json.dumps(output, indent=4)

    def testGetAbortedTaskList(self):
        output = self.aggregator.get_aborted_task_list()
        #print json.dumps(output, indent=4)





