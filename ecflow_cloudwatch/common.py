import argparse
import boto3
import json

def parse_args():
    """parse command line argument"""
    parser = argparse.ArgumentParser(description='Put ecFlow metrics to cloudwatch')
    parser.add_argument('--namespace', help='The namespace for the metric data. (default: ecflow)', \
                           default="ecflow")
    parser.add_argument('--environment', help='Specify environment, it will get add in dimensions with Env key', required=True)
    parser.add_argument('--ecflow_port', help='ecflow server port', \
                           default="3143")
    parser.add_argument('--ecflow_host', help='ecflow server host ip or hostname', \
                           default="localhost")
    parser.add_argument('--fetch_new', help='Filter only current and future cycle data from ecflow defs', \
                           default='False', choices=('True','False'))
    args = parser.parse_args()
    return args


def put_metric_data(data,namespace=None):
    """
    Publish data into cloudwatch
    """
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.put_metric_data(
            MetricData = data,
            Namespace = namespace
            )
    return response
