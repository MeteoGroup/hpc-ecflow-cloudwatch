from EcflowDAO import EcflowDAO
from ecflow_state_parser import EcflowStateParser
from metric_aggregator import MetricAgregator
from metric_converter import MetricsConverters


class EcflowMetrics(object):

    def get_ecflow_metrics(self):
        dao = EcflowDAO()
        output = dao.fetch_ecflow_stats()
        parser = EcflowStateParser()
        metrics = parser.parse_ecflow_state(output)
        aggregator = MetricAgregator()
        aggregated_metrics = aggregator.aggregate_raw_metrics(metrics)

        converter = MetricsConverters()
        prometheus_dict = converter.convert_to_prometheus_format(aggregated_metrics)

        output_str = ""
        for key, value in prometheus_dict.iteritems():
            output_str = output_str+"\n"+key+" "+str(value)

        return output_str
