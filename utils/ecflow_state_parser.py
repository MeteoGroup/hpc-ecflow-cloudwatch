class EcflowStateParser(object):

    metric_prefix = "ecflow"
    metrics = {}

    def parse_ecflow_state(self,rawinput):
        last_prefix = ""
        last_part = ""
        lines = rawinput.splitlines()
        for line in lines:

            parts = self.preprocess_line(line)

            if parts[0] == "suite" or parts[0] == "family" or parts[0] == 'task':
                self.metric_prefix = self.metric_prefix + "_" + parts[1]

                if parts[0] == "task":
                    if last_part == "task":
                        self.metric_prefix = self.metric_prefix.replace("_"+last_prefix, "")

                n = 0
                for part in parts:
                    if part == "state":
                        break
                    n = n + 1

                self.metrics[self.metric_prefix] = parts[n+1]

                last_prefix = parts[1]
                last_part = parts[0]

            if parts[0] == "endsuite" or parts[0] == "endfamily":
                self.metric_prefix = self.metric_prefix.replace("_"+last_prefix, "")

        print self.metric_prefix
        print self.metrics



    def preprocess_line(self,line):
        # remove leading and trailing spaces
        line = line.strip()

        # replace colon by space
        line = line.replace(":"," ")
        # split line by space
        parts = line.split(" ")
        return parts