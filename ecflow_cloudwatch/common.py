import argparse
import boto3
from subprocess import Popen, PIPE
import json

def parse_args():
    """parse command line argument"""
    parser = argparse.ArgumentParser(description='Put ecFlow metrics to cloudwatch')
    parser.add_argument('--dimensions', help='identity of a metric using a Name=Value pair, \
                         separated by commas', required=True)
    parser.add_argument('--namespace', help='The namespace for the metric data. (default: ecFlow)', \
                           default="ecFlow")
    args = parser.parse_args()
    return args


def prepared_dimensions(dimensions):
    """
    Parse User input string e.g key=value as dict
    """
    values = dict([ value.split("=") for value in dimensions.split(",") if len(value.split("=")) == 2 ])
    dimensions_list = []
    for k,v in values.items():
      dimensions_list.append({
             "Name": k,
             "Value": v
          })
    return dimensions_list


def get_cmd_output(cmd):
    """Execute the command and return its output"""
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr != "":
        raise ValueError("Unable to run {0}, Error: {1}".format(cmd,stderr))
    return stdout


def prepare_cloudwatch_metrics(data={},dimensions=[]):
    """
    Prepare cloudwatch json using dict input,
    namespace and dimensions
    """
    dimensions = prepared_dimensions(dimensions)
    metrics_data = []
    # extract key, value(0), unit(1)
    for key, value in data.items():
        metrics_data.append({
                  "MetricName": key,
                  "Dimensions": dimensions,
                  "Unit":  value[1],
                  "Value": value[0]
                })
    return metrics_data

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