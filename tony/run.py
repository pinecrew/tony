import subprocess

def run_cmd(cmd):
    if cmd is None:
        return
    proc = subprocess.run(cmd, shell=True, capture_output=True)
    stdout = proc.stdout.decode('utf8').strip()
    stderr = proc.stderr.decode('utf8').strip()
    if proc.returncode != 0:
        print(f'===\nstderr\n===\n{stderr}\n---')
        print(f'===\nstdout\n===\n{stdout}\n---')
        raise ValueError(f'Command failed with code {proc.returncode}')
    else:
        print(f'===\nstdout\n===\n{stdout}\n')

def build(config, target):
    # increment build version
    config['project', 'build'] += 1
    config.save()

    # run all
    run_cmd(config['build', target, 'before'])
    run_cmd(config['build', target, 'cmd'])
    run_cmd(config['build', target, 'after'])

def test(config):
    run_cmd(config['test', 'before'])
    run_cmd(config['test', 'cmd'])
    run_cmd(config['test', 'after'])