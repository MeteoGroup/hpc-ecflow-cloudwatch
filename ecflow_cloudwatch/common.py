import argparse
import boto3
from subprocess import Popen, PIPE
import json

def parse_args():
    """parse command line argument"""
    parser = argparse.ArgumentParser(description='Put ecFlow metrics to cloudwatch')
    parser.add_argument('--namespace', help='The namespace for the metric data. (default: Dev/ecFlow)', \
                           default="Dev/ecFlow")
    parser.add_argument('--ecflow_port', help='ecflow server port', \
                           default="3143")
    parser.add_argument('--ecflow_host', help='ecflow server host ip or hostname', \
                           default="localhost")
    parser.add_argument('--fetch_new', help='Filter only current and future cycle data from ecflow defs', \
                           default="False")
    args = parser.parse_args()
    return args



def get_cmd_output(cmd):
    """Execute the command and return its output"""
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr != "":
        raise ValueError("Unable to run {0}, Error: {1}".format(cmd,stderr))
    return stdout


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