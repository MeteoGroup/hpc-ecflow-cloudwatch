import subprocess

class MetricAgregator(object):

    def __init__(self, metrics, default_dimensions):
        self.metrics = metrics
        self.agregated_metrics = {}
        self.aborted_tasks = 0
        self.suspended_tasks = 0
        self.queued_tasks = 0
        self.running_tasks = 0
        self.completed_tasks = 0
        self.default_dimensions = self.prepared_dimensions(default_dimensions)

    def get_counts(self, dimentions=[]):
        for svc in self.metrics:
            for key, value in svc.items():

                if "status" in key:
                    if value == "aborted":
                        self.aborted_tasks +=  1

                    if value == "suspended":
                        self.suspended_tasks +=  1

                    if value == "queued":
                        self.queued_tasks +=  1

                    if value == "active":
                        self.running_tasks +=  1

                    if value == "complete":
                        self.completed_tasks +=  1

            self.agregated_metrics['aborted_tasks'] = self.aborted_tasks
            self.agregated_metrics['suspended_tasks'] = self.suspended_tasks
            self.agregated_metrics['queued_tasks'] = self.queued_tasks
            self.agregated_metrics['running_tasks'] = self.running_tasks
            self.agregated_metrics['completed_tasks'] = self.completed_tasks

        return self.agregated_metrics

    def percentage(self, part, whole):
        if part == 0 and whole == 0:
            return 0
        return 100 * float(part)/float(whole)

    def prepared_dimensions(self, dimensions):
        """
        Convert dict to cloudwatch formate dimension data
        """
        dimensions_data = []
        for key, value in dimensions.iteritems():
            dimensions_data.append(dict(
                Name=key,
                Value=value
            ))
        return dimensions_data

    def prepare_cloudwatch_metrics(self, data={}, unit='Count', dimensions=[], stats={}):
        """
        Prepare cloudwatch json using dict input,
        namespace and dimensions
        """
        for default_dimension in self.default_dimensions:
            if default_dimension not in dimensions:
                dimensions.append(default_dimension)
        metrics_data = dict(
                MetricName=data.keys()[0],
                Value=data.values()[0],
                Unit=unit,
                Dimensions=dimensions
            )
        if stats:
            metrics_data['StatisticValues']=stats
            # the parameters MetricData.member.1.Value and MetricData.member.1.StatisticValues are mutually exclusive and you have specified both
            del metrics_data['Value']
        return metrics_data

    def get_metrics_counts(self):
        counts = self.get_counts()
        return [self.prepare_cloudwatch_metrics({k:v}) for k,v in counts.iteritems()]

    def get_running_threads(self):
        procs = subprocess.check_output(['ps', 'auwx']).splitlines()
        data = dict(
            running_threads = len([proc for proc in procs if 'ecflow_server' in proc])
        )
        return [self.prepare_cloudwatch_metrics(data)]

    def get_metrics_meters(self):
        cloud_watch_metrics = []
        for svc in self.metrics:
            if "progress" in svc and "-1" in svc["progress"]:
                _, maximum, value = map(int, svc['progress'].split(","))
                # change -1 to 0, cloudwatch does not support negative int
                if value < 0:
                    value = 0
                metrics_data = {svc['datasource']: self.percentage(value, maximum)}
                # with different progress value cloudwatch create new metrics instead of updating exsting
                # to fix this remove progress from metrics
                del svc['progress']
                # remove datasource key because, already sending as metrics name
                del svc['datasource']
                dimensions = self.prepared_dimensions(svc)
                cloud_watch_metrics.append(self.prepare_cloudwatch_metrics(
                    data=metrics_data,
                    unit="Percent",
                    dimensions=dimensions))
        return cloud_watch_metrics

    def get_aborted_task_list(self):
        cloud_watch_metrics = []
        for svc in self.metrics:
            for key, value in svc.items():
                if "status" in key:
                    if value == "aborted":
                        try:
                            if 'datasource_task' in  svc.keys():
                                metrics_data = {svc['datasource_task']:1}
                            else:
                                metrics_data  = {svc['task']:1}
                            dimensions = self.prepared_dimensions(svc)
                            cloud_watch_metrics.append(self.prepare_cloudwatch_metrics(
                                data=metrics_data,
                                unit="Count",
                                dimensions=dimensions))
                        except Exception as e:
                            print(str(svc))
                            print(str(e))
                            pass
        return cloud_watch_metrics









