import toml
import sys
import glob
import time
import os


class Config:
    def __init__(self, filename):
        self.filename = filename
        self.config = self.load(filename)

    def load(self, filename):
        try:
            return toml.load(filename)
        except:
            print(sys.exc_info()[1])
            exit()

    def save(self):
        try:
            toml.dump(self.config, open(self.filename, 'w'))
        except:
            print(sys.exc_info()[1])
            exit()

    def env_vars(self):
        result = os.environ.copy()
        for key, value in self.config['project'].items():
            result['PROJECT_' + key.upper()] = str(value)
        return result

    def __getitem__(self, key_chain):
        if not isinstance(key_chain, tuple):
            return self.config[key_chain]
        item = self.config
        for key in key_chain:
            item = item.get(key)
            if item is None:
                return item
        return item

    def __setitem__(self, key_chain, value):
        if not isinstance(key_chain, tuple):
            self.config[key_chain] = value
        item = self.config
        for key in key_chain[:-1]:
            item = item[key]
        item[key_chain[-1]] = value

    def bump_version(self, part):
        major, minor, bugfix = map(int, self['project', 'version'].split('.'))
        # increment version
        if part == 'major':
            major += 1
            minor = 0
            bugfix = 0
        elif part == 'minor':
            minor += 1
            bugfix = 0
        elif part == 'bugfix':
            bugfix += 1
        self['project', 'version'] = f'{major}.{minor}.{bugfix}'

    def fill_variables(self):
        templates = glob.glob('./**/*.template', recursive=True)
        for template in templates:
            contents = ''
            with open(template, 'r') as f:
                contents = f.read()
            fname = '.'.join(template.split('.')[:-1])
            with open(fname, 'w') as f:
                f.write(contents.format(timestamp=int(
                    time.time()), **self['project']))
