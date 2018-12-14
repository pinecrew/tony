#!/usr/bin/env python
import argparse
import toml
import sys


def tony_build(target, filename):
    if isinstance(filename, str):
        config = toml.load(filename)
    elif isinstance(filename, dict):
        config = filename
    else:
        raise ValueError('Malformed config')
    print('build:', target)
    print('config:', config)
    return True


def tony_bump(part, filename):
    if isinstance(filename, str):
        config = toml.load(filename)
    elif isinstance(filename, dict):
        config = filename
    else:
        raise ValueError('Malformed config')
    print('bump:', part)
    print('config:', config)
    # ...
    # bump
    # ...
    tony_build('release', config)
    tony_test(config)
    return True


def tony_package(filename):
    if isinstance(filename, str):
        config = toml.load(filename)
    elif isinstance(filename, dict):
        config = filename
    else:
        raise ValueError('Malformed config')
    print('package')
    print('config:', config)
    return True


def tony_test(filename):
    if isinstance(filename, str):
        config = toml.load(filename)
    elif isinstance(filename, dict):
        config = filename
    else:
        raise ValueError('Malformed config')
    print('test')
    print('config:', config)
    return True


def main():
    filename = 'project.toml'

    parser = argparse.ArgumentParser(description='Tony Build System')
    subparser = parser.add_subparsers()
    build = subparser.add_parser('build', help='build current project')
    build.add_argument('--build', choices=['debug', 'release'], default='debug', required=False)
    bump = subparser.add_parser('bump', help='bump this shit')
    bump.add_argument('--bump', choices=['major', 'minor', 'bugfix'], default='bugfix', required=False)
    package = subparser.add_parser('package', help='pack your project into archive')
    package.add_argument('--package', default=True, required=False)
    test = subparser.add_parser('test', help='test your shitty code')
    test.add_argument('--test', default=True, required=False)
    args = parser.parse_args()
    if args == argparse.Namespace():
        parser.print_help()
        exit()
    else:
        try:
            if hasattr(args, 'build'):
                tony_build(args.build, filename)
            elif hasattr(args, 'bump'):
                tony_bump(args.bump, filename)
            elif hasattr(args, 'package'):
                tony_package(filename)
            elif hasattr(args, 'test'):
                tony_test(filename)
        except:
            print(sys.exc_info()[1])
            exit()

if __name__ == '__main__':
    main()