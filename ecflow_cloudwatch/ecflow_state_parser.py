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
            "datafetcher": ["suite", "cycle_time", "service", "datasource_task", "status"],
            "dataconversion": ["suite", "cycle_time", "service", "datasource", "task", "status"],
            "mgmodels": ["suite", "cycle_time", "service" ,"model", "area", "task", "status"],
            "default": ["suite", "cycle_time", "service", "state"]
        },
        "crontab": {
             "default": ["suite", "service", "task", "state"]
        }
    }

    metrics = []

    def __init__(self, defs):
        assert (isinstance(defs, ecflow.Defs)),"Expected ecflow.Defs as first argument"
        self.__defs = defs

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
        suite = task_path[0]
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
        state_key = data_format[-1]
        state = data_set[-1]
        data_format_copy = data_format[:-1]
        data_set_copy = data_set[:-1]
        for i in range(len(data_format_copy)):
            # exclude key which has - char 
            #print data_format[i]
            if '-' in data_format_copy[i]:
                continue
            if data_format_copy[i] == data_format_copy[-1]:
                 data_set_copy[i] = "_".join(data_set_copy[i:])
            output.append((data_format_copy[i],data_set_copy[i]))
        output.append((state_key, state))
        output.append(('task_path', '/'.join(data_set_copy)))
        return dict(output)
    
    def parse(self):
        for suite in self.__defs.suites:
                for service in suite.nodes:
                    for task in service.get_all_nodes():
                        if self.is_task(task) or self.is_meter(task):
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