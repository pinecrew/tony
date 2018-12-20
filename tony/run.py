import subprocess
import os


def run_cmd(cmd):
    if cmd is None:
        return
    if isinstance(cmd, str):
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            while proc.poll() is None:
                print(proc.stdout.readline().decode('utf8'), end='')
            if proc.returncode != 0:
                stderr = proc.stderr.read().decode('utf8').strip()
                print(f'===\nstderr\n===\n{stderr}\n---')
                print(f'[error]: command failed with code {proc.returncode}')
                exit(-1)
    elif isinstance(cmd, list):
        for item in cmd:
            run_cmd(item)
    else:
        print(f'unsupported type of cmd {type(cmd)}')
        exit(-1)


def build(config, target):
    # increment build version
    config['project', 'build'] += 1
    config.save()
    config.fill_variables()
    print('[info] start building process')
    print('[info] version {version}, build {build}'.format(**config['project']))
    # run all
    run_cmd(config['build', target, 'before'])
    run_cmd(config['build', target, 'cmd'])
    run_cmd(config['build', target, 'after'])


def test(config):
    print('[info] start testing process')
    run_cmd(config['test', 'before'])
    run_cmd(config['test', 'cmd'])
    run_cmd(config['test', 'after'])

def package(config):
    print('[info] start packaging')
    if os.path.exists('package') and os.path.isdir('package'):
        pass
    else:
        print('[error] package directory not found')