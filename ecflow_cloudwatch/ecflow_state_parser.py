import re
import sys
import json
import ecflow
import logging 
from datetime import datetime


class EcflowStateParser(object):

    # config for strcutre data 
    # if key has - sign, it will exclude from parsing 
    # By default, it will also add path of task 
    services = {
        "mgforecast" : {
            "controller": ["suite", "service", "task", "state"],
            "monitor": ["suite", "cycle_time-", "service", "datasource", "progress"],
            "datafetcher": ["suite", "cycle_time-", "service", "datasource_task", "status"],
            "dataconversion": ["suite", "cycle_time-", "service", "datasource", "task", "status"],
            "mgmodels": ["suite", "cycle_time-", "service" ,"model", "area", "task", "status"],
            "default": ["suite", "cycle_time-", "service", "state"]
        },
        "crontab": {
             "default": ["suite", "service", "task", "state"]
        }
    }

    cycletime_format = "(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})"
    cycletime_date_format = "%Y%m%d%H%M"

    metrics = []

    def __init__(self, defs, fetch_new):
        assert (isinstance(defs, ecflow.Defs)),"Expected ecflow.Defs as first argument"
        self.__defs = defs
        # fetch new data only
        self.fetch_new = fetch_new

    # Cloudwatch needed uniq metrics and due to forecast hour with date in each task
    # it can't be uniq, so extracting only forecast hour from date
    def convert_to_forecast_hour(self, data):
        match = re.search(self.cycletime_format, data)
        if match:
            match_date = datetime.strptime(match.group(), self.cycletime_date_format)
            return str(match_date.hour)

    # parse data only with current and future date
    def filter_date(self, node):
        if self.fetch_new:
            present = datetime.strptime(
                datetime.now().replace(minute=0, second=0, microsecond=0).strftime(self.cycletime_date_format),
                self.cycletime_date_format)
            match = re.search(self.cycletime_format, node)
            if match:
                this_date = datetime.strptime(match.group(), self.cycletime_date_format)
                hours_diff = (present - this_date).total_seconds() / 3600
                if hours_diff < 4 and hours_diff >= 0:
                    #print "{} >= {}".format(this_date, present)
                    return True
            else:
                # if node does not have cycledate this return as it is
                return True
        return False
        
        
    def is_task(self, node):
        if isinstance(node, ecflow.Task):
            return True
        return False

    def is_meter(self, node):
        for meter in node.meters:
            if meter.value():
                return True
        return False

    def select_service(self, task_path):
        # extract suite e.g. mgforecast or hindcast
        suite = task_path[0]
        # if suite configuired 
        if suite in self.services.keys():
            for task in task_path:
                    if task in self.services[suite].keys():
                        return self.services[suite][task]
            return self.services[suite]['default']
        else:
            return None


    def combine(self, data_format, data_set):
        # if len(x) == len(y):
        #     return dict(zip(x,y))
        output = []
        # extract header eg. state or progress 
        state_key = data_format[-1]
        # extract last field data as status
        state = data_set[-1]

        # make copy excluding last field to modify 
        data_format_copy = data_format[:-1]
        data_set_copy = data_set[:-1]
        for i in range(len(data_format_copy)):
            # Role 1# exclude key which has - char
            if '-' in data_format_copy[i]:
                continue
            # Rule 3# Remaning data join with underscore and convert cycledate to forecast hour
            if data_format_copy[i] == data_format_copy[-1]:
                 data_set_copy[i] = "_".join(self.convert_to_forecast_hour(d) if self.convert_to_forecast_hour(d) else d for d in data_set_copy[i:])
            output.append((data_format_copy[i],data_set_copy[i]))
        output.append((state_key, state))
        #output.append(('task_path', '/'.join(data_set_copy)))
        return dict(output)
    
    def parse(self):
        for suite in self.__defs.suites:
                for service in suite.nodes:
                    for task in service.get_all_nodes():
                        if self.is_task(task) or self.is_meter(task):
                            if self.filter_date(task.get_abs_node_path()):
                                #print("Parsing {}".format(task.get_abs_node_path()))
                                available_data = filter(None, task.get_abs_node_path().split("/"))
                                selected_data = self.select_service(available_data)

                                if selected_data is None:
                                    print "Missing configs for {} {}".format(suite.name(), task.get_abs_node_path())
                                    continue

                                if self.is_meter(task):
                                    for meter in task.meters:
                                        min, max, threshold = meter.min(), meter.max(), meter.value()
                                    available_data.append(','.join(map(lambda x: str(x), [min, max, threshold])))
                                else:
                                    available_data.append(str(task.get_state()))


                                try:
                                    metric = self.combine(selected_data, available_data)
                                    self.metrics.append(metric)
                                except:
                                    if selected_data and available_data:
                                        metric = self.combine(selected_data, available_data)
                                        self.metrics.append(metric)
                                    else:
                                        print "Unable to parse data:"
                                        print task.get_abs_node_path()
                                        raise

        return self.metrics