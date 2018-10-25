class EcflowStateParser(object):

    metric_prefix = "ecflow"
    metrics = {}

    def parse_ecflow_state(self,rawinput):
        last_prefix = ""
        family_prefix = []
        last_suite_prefix = ""
        last_part = ""
        lines = rawinput.splitlines()
        for line in lines:

            parts = self.preprocess_line(line)

            if parts[0] == "suite" or parts[0] == "family" or parts[0] == 'task':
                self.metric_prefix = self.metric_prefix + "_" + parts[1]

                if parts[0] == "task":
                    if last_part == "task":
                        # task has no end task tag
                        self.metric_prefix = self.metric_prefix.replace("_"+last_prefix, "")

                    self.metric_prefix = self.metric_prefix + "_task"
                    last_prefix = parts[1] + "_task"

                if parts[0] == "family":
                    if last_part == "task":
                        # task can be followed by a family
                        self.metric_prefix = self.metric_prefix.replace("_"+last_prefix, "")
                    family_prefix.append(parts[1])

                if parts[0] == "suite":
                    last_suite_prefix = parts[1]

                n = 0
                for part in parts:
                    if part == "state":
                        break
                    n = n + 1

                self.metrics[self.metric_prefix] = parts[n+1]

                last_part = parts[0]

            if parts[0] == "endfamily":
                if last_part == "task":
                    self.metric_prefix = self.metric_prefix.replace("_"+family_prefix[-1]+"_"+last_prefix, "")
                elif last_part == "endfamily" or last_part == "family":
                    self.metric_prefix = self.metric_prefix.replace("_" + family_prefix[-1], "")

                del family_prefix[-1]
                last_part = parts[0]

            if parts[0] == "endsuite":
                self.metric_prefix = self.metric_prefix.replace("_"+last_suite_prefix, "")

        return self.metrics

    def preprocess_line(self,line):
        # remove leading and trailing spaces
        line = line.strip()

        # replace colon by space
        line = line.replace(":"," ")
        # split line by space
        parts = line.split(" ")
        return parts