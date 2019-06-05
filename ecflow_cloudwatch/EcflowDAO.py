from external import run_subprocess


class EcflowDAO(object):

    def fetch_ecflow_stats(self):
        command = "module load ecflow/gcc/4.11.0 &&  ecflow_client --get_state"
        raw_stats = run_subprocess(command)
        return raw_stats

