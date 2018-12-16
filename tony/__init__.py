#!/usr/bin/env python
import subprocess
import argparse
import toml
import sys


def load_config(filename):
    try:
        return toml.load(filename)
    except:
        print(sys.exc_info()[1])
        exit()


def save_config(config, filename):
    try:
        toml.dump(config, open(filename, 'w'))
    except:
        print(sys.exc_info()[1])
        exit()


def get_param(config, lst):
    item = config
    for key in lst:
        item = item.get(key)
        if item is None:
            return item
    return item


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


def build_handler(args):
    if args.debug:
        print('target:', args.target)
        print('config:', args.file)

    # increment build version
    config = load_config(args.file)
    config['project']['build'] += 1
    save_config(config, args.file)

    # build process
    p_before = get_param(config, ('build', args.target, 'before'))
    p_cmd = get_param(config, ('build', args.target, 'cmd'))
    p_after = get_param(config, ('build', args.target, 'after'))

    # run all
    run_cmd(p_before)
    run_cmd(p_cmd)
    run_cmd(p_after)

    return True


def bump_handler(args):
    if args.debug:
        print('bump:', args.part)
        print('config:', args.file)

    config = load_config(args.file)
    major, minor, bugfix = map(int, config['project']['version'].split('.'))
    # increment version
    if args.part == 'major':
        major += 1
    elif args.part == 'minor':
        minor += 1
    elif args.part == 'bugfix':
        bugfix += 1
    config['project']['version'] = f'{major}.{minor}.{bugfix}'
    save_config(config, args.file)

    # do other stuff
    build_handler(args)
    test_handler(args)
    return True


def package_handler(args):
    if args.debug:
        print('package')
        print('config:', args.file)
    return True


def test_handler(args):
    if args.debug:
        print('test')
        print('config:', args.file)

    config = load_config(args.file)

    # test process
    p_before = get_param(config, ('test', 'before'))
    p_cmd = get_param(config, ('test', 'cmd'))
    p_after = get_param(config, ('test', 'after'))

    # run all
    run_cmd(p_before)
    run_cmd(p_cmd)
    run_cmd(p_after)
    return True


def new_handler(args):
    if args.debug:
        print('new')
        print('config:', args.file)
    return True


def init_handler(args):
    if args.debug:
        print('init')
        print('config:', args.file)
    return True


def main():
    parser = argparse.ArgumentParser(description='Tony Build System')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-d', '--debug', help='print debug info', action='store_true')
    parser.add_argument('-f', '--file', help='specify configuration file', default='project.toml')
    parser.set_defaults(handler=lambda args: parser.print_help())

    subparser = parser.add_subparsers()

    build = subparser.add_parser('build', help='build current project')
    build.add_argument('target', nargs='?', choices=['debug', 'release'], default='debug')
    build.set_defaults(handler=build_handler)

    bump = subparser.add_parser('bump', help='bump this shit')
    bump.add_argument('version', nargs='?', choices=['major', 'minor', 'bugfix'], default='bugfix')
    bump.set_defaults(handler=bump_handler)

    package = subparser.add_parser('package', help='pack your project into archive')
    package.set_defaults(handler=package_handler)

    test = subparser.add_parser('test', help='test your shitty code')
    test.set_defaults(handler=test_handler)

    new = subparser.add_parser('new', help='create empty project')
    new.add_argument('name', nargs=1)
    new.set_defaults(handler=new_handler)

    init = subparser.add_parser('init', help='initialize project in current directory')
    init.add_argument('name', nargs='?', default=None)
    init.set_defaults(handler=init_handler)

    args = parser.parse_args()
    if args.debug:
        print('args:', args)
    args.handler(args)


if __name__ == '__main__':
    main()
