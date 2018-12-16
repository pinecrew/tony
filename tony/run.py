import subprocess


def run_cmd(cmd):
    if cmd is None:
        return
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        while proc.poll() is None:
            print(proc.stdout.readline().decode('utf8').strip())
        if proc.returncode != 0:
            stderr = proc.stderr.read().decode('utf8').strip()
            print(f'===\nstderr\n===\n{stderr}\n---')
            print(f'[error]: command failed with code {proc.returncode}')
            exit(-1)


def build(config, target):
    # increment build version
    config['project', 'build'] += 1
    config.save()

    print('[info] start building process')

    # run all
    run_cmd(config['build', target, 'before'])
    run_cmd(config['build', target, 'cmd'])
    run_cmd(config['build', target, 'after'])


def test(config):
    print('[info] start testing process')
    run_cmd(config['test', 'before'])
    run_cmd(config['test', 'cmd'])
    run_cmd(config['test', 'after'])
