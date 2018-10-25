class MetricAgregator(object):

    agregated_metrics = {}
    nr_aborted_tasks = 0
    nr_suspended_tasks = 0
    nr_queued_tasks = 0
    nr_running_tasks = 0

    def aggregate_raw_metrics(self,raw_metrics):

        for key, value in raw_metrics.items():
            if "task" in key:
                if value == "aborted":
                    self.nr_aborted_tasks = self.nr_aborted_tasks + 1

                if value == "suspended":
                    self.nr_suspended_tasks = self.nr_suspended_tasks + 1

                if value == "queued":
                    self.nr_queued_tasks = self.nr_queued_tasks + 1

                if value == "running":
                    self.nr_running_tasks = self.nr_running_tasks + 1

        self.agregated_metrics['aborted_tasks'] = self.nr_aborted_tasks
        self.agregated_metrics['suspended_tasks'] = self.nr_suspended_tasks
        self.agregated_metrics['queued_tasks'] = self.nr_queued_tasks
        self.agregated_metrics['running_tasks'] = self.nr_running_tasks

        final_metrics = self.agregated_metrics.copy()
        final_metrics.update(raw_metrics)

        return final_metrics
