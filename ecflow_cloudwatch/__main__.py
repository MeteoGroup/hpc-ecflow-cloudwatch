import os
from distutils.util import strtobool
import ecflow
from common import parse_args
from common import put_metric_data

from ecflow_client_utils import GetEcflowStats
from ecflow_state_parser import EcflowStateParser
from metric_aggregator import MetricAgregator

def get_ecflow_metrics(fetch_new):
    # Get data
    ecf_client = GetEcflowStats()
    ecf_defs = ecf_client.fetch_ecflow_stats()
    # parse to json
    parser = EcflowStateParser(ecf_defs, fetch_new=fetch_new)
    return parser.parse()


def main():
    args = parse_args()
    namespace = args.namespace
    environment = args.environment
    ecf_host = args.ecflow_host
    ecf_port = args.ecflow_port
    fetch_new = bool(strtobool(args.fetch_new))

    dimensions = dict(Env=environment)

    metrics = get_ecflow_metrics(fetch_new)
    aggregator = MetricAgregator(metrics, dimensions)
    counts = aggregator.get_metrics_counts()
    meters = aggregator.get_metrics_meters()
    aborted_task_list = aggregator.get_aborted_task_list()
    running_threads = aggregator.get_running_threads()

    for ecflow_data in counts + meters + aborted_task_list + running_threads:
        put_metric_data([ecflow_data], namespace)


if __name__ == '__main__':
    main()




