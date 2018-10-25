class MetricsConverters(object):
    prometheus_dict = {}

    def convert_ecflow_state_to_nr(self,argument):
        switcher = {
            'unknown' : 0,
            'complete': 1,
            'running': 2,
            'queued': 3,
            'suspended': 4,
            'aborted' : 5
        }
        return switcher.get(argument, "Invalid month")

    def convert_to_prometheus_format(self,metrics_dict):
        for key, value in metrics_dict.items():
            if isinstance(value, basestring):
                self.prometheus_dict[key+'{label="'+value+'"}']=self.convert_ecflow_state_to_nr(value)
            else:
                self.prometheus_dict[key] = value
        return self.prometheus_dict