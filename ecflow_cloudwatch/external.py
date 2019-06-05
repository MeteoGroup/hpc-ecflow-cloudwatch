from subprocess import check_output, CalledProcessError, STDOUT


def run_subprocess(cmd, shell=True):
    try:
        return check_output(cmd, shell=shell)
    except CalledProcessError as e:
        print('{} failed:'.format(cmd))
        print(e)
        raise
