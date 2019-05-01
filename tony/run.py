import colorama as cl
import subprocess
import os


def run_cmd(cmd, env=None):
    if cmd is None:
        return
    if isinstance(cmd, str):
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env) as proc:
            while proc.poll() is None:
                print(proc.stdout.readline().decode('utf8'), end='')
            if proc.returncode != 0:
                stderr = proc.stderr.read().decode('utf8').strip()
                print('========\n' + cl.Fore.RED + ' stderr\n' + cl.Fore.WHITE + f'========\n{stderr}\n-------')
                print('[' + cl.Fore.RED + 'error' + cl.Fore.WHITE + f']: command failed with code {proc.returncode}')
                exit(-1)
    elif isinstance(cmd, list):
        for item in cmd:
            run_cmd(item, env)
    else:
        print('[' + cl.Fore.RED + 'error' + cl.Fore.WHITE + f'] unsupported type of cmd {type(cmd)}')
        exit(-1)


def build(config, target):
    # increment build version
    config['project', 'build'] += 1
    config.save()
    config.fill_variables()
    print('[' + cl.Fore.GREEN + 'info' + cl.Fore.WHITE + '] start building process')
    print('[' + cl.Fore.GREEN + 'info' + cl.Fore.WHITE +
          '] version {version}, build {build}'.format(**config['project']))
    # run all
    for i in ['before', 'cmd', 'after']:
        run_cmd(config['build', target, i], config.env_vars())


def test(config):
    print('[' + cl.Fore.GREEN + 'info' + cl.Fore.WHITE + '] start testing process')
    for i in ['before', 'cmd', 'after']:
        run_cmd(config['test', i], config.env_vars())


def clean(config):
    print('[' + cl.Fore.GREEN + 'info' + cl.Fore.WHITE + '] start cleaning process')
    for i in ['before', 'cmd', 'after']:
        run_cmd(config['clean', i], config.env_vars())


def package(config):
    print('[' + cl.Fore.GREEN + 'info' + cl.Fore.WHITE + '] start packaging')
    if not config['package', 'packager']:
        print('[' + cl.Fore.RED + 'error' +
              cl.Fore.WHITE + '] packager is not specified')
        return
    packager = config['package', 'packager']
    if os.path.exists(packager):
        run_cmd(packager, config.env_vars())
    else:
        print('[' + cl.Fore.RED + 'error' + cl.Fore.WHITE + f'] {packager} not found')
