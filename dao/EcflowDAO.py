from external import run_subprocess


class EcflowDAO(object):

    def fetch_ecflow_stats(self):
        command = "cd /home/vagrant/Documents/hpc-ecflow-cloudwatch && module load ecflow/intel/4.7.1 &&  ecflow_client --get_state"
        raw_stats = run_subprocess(command)
        return raw_stats

