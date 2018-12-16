#!/usr/bin/env python
import argparse

from .config import Config
from .run import test, build


def build_handler(args):
    if args.debug:
        print('target:', args.target)
        print('config:', args.file)
    config = Config(args.file)
    build(config, args.target)


def bump_handler(args):
    if args.debug:
        print('bump:', args.part)
        print('config:', args.file)

    config = Config(args.file)
    config.bump_version(args.part)
    config.save()

    # do other stuff
    build(config, 'release')


def package_handler(args):
    if args.debug:
        print('package')
        print('config:', args.file)


def test_handler(args):
    if args.debug:
        print('test')
        print('config:', args.file)
    config = Config(args.file)
    build(config, 'debug')
    test(config)


def new_handler(args):
    if args.debug:
        print('new')
        print('config:', args.file)


def init_handler(args):
    if args.debug:
        print('init')
        print('config:', args.file)


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
    bump.add_argument('part', nargs='?', choices=['major', 'minor', 'bugfix'], default='bugfix')
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
