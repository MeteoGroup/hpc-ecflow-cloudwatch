from .common import parse_args
from .common import prepare_cloudwatch_metrics
from .common import put_metric_data

from EcflowDAO import EcflowDAO
from ecflow_state_parser import EcflowStateParser
from metric_aggregator import MetricAgregator
from metric_converter import MetricsConverters


def get_ecflow_metrics():
    dao = EcflowDAO()
    output = dao.fetch_ecflow_stats()
    parser = EcflowStateParser()
    metrics = parser.parse_ecflow_state(output)
    aggregator = MetricAgregator()
    aggregated_metrics = aggregator.aggregate_raw_metrics(metrics)

    return aggregated_metrics

def main():
    args = parse_args()
    dimensions = args.dimensions
    namespace = args.namespace

    ecflow_data = prepare_cloudwatch_metrics(get_ecflow_metrics(), dimensions)
    put_metric_data(ecflow_data, namespace)

    


