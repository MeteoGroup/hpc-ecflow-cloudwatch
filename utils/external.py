import subprocess


def run_subprocess(cmd, shell=True):
    try:
        return subprocess.check_output(cmd, shell=shell, stderr=subprocess.STDOUT)
    except:
        print('{} failed:'.format(cmd))
        raise
