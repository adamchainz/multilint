# -*- encoding:utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import subprocess
import sys

if sys.version_info[0] == 2:
    from cStringIO import StringIO
    from ConfigParser import SafeConfigParser  # Py 2
else:
    from configparser import SafeConfigParser  # Py 3
    from io import StringIO

try:
    from flake8.main.cli import main as flake8_main  # flake8 3+
except ImportError:
    try:
        from flake8.main import main as flake8_main  # flake8 <3
    except ImportError:
        flake8_main = None

try:
    from isort.main import main as isort_main
except ImportError:
    isort_main = None

try:
    from libmodernize.main import main as libmodernize_main
except ImportError:
    libmodernize_main = None

__author__ = 'Adam Johnson'
__email__ = 'me@adamj.eu'
__version__ = '2.0.1'


def main():
    settings = load_settings()

    ret = check_settings(settings)
    if ret:
        return ret

    ret = run_flake8(settings['paths'])
    if ret:
        return ret

    ret = run_modernize(settings['paths'])
    if ret:
        return ret

    ret = run_isort(settings['paths'])
    if ret:
        return ret

    # Broken on 2.7.9 due to http://bugs.python.org/issue23063
    if sys.version_info[:3] != (2, 7, 9):
        ret = run_setup_py_check()
        if ret:
            return ret

    return 0


MAX_CONFIG_SEARCH_DEPTH = 25
default_settings = {
    'paths': []
}


def load_settings():
    settings = default_settings.copy()
    _update_settings_from_file('setup.cfg', settings)
    return settings


def _update_settings_from_file(section, settings):
    tries = 0
    current_directory = os.path.normpath(os.getcwd())
    while current_directory and tries < MAX_CONFIG_SEARCH_DEPTH:
        potential_path = os.path.join(current_directory, 'setup.cfg')
        if os.path.exists(potential_path):
            config_file = potential_path
            break

        new_directory = os.path.split(current_directory)[0]
        if current_directory == new_directory:
            break
        current_directory = new_directory
        tries += 1

    if config_file and os.path.exists(config_file):
        with open(config_file, 'rU') as fp:
            config = SafeConfigParser()
            config.readfp(fp)
        if config.has_section('tool:multilint'):
            settings.update(sanitize(config.items('tool:multilint')))


def sanitize(config_items):
    output = {}
    for key, value in dict(config_items).items():
        if key in default_settings:
            if isinstance(default_settings[key], list):
                value = [v.strip() for v in value.split('\n') if v.strip()]
            output[key] = value
    return output


def check_settings(settings):
    if not settings['paths']:
        print(
            'No paths defined in [tool:multilint] section in setup.cfg',
            file=sys.stderr,
        )
        return 1

    all_exist = True
    for path in settings['paths']:
        if not os.path.exists(path):
            all_exist = False
            print('Path {} does not exist'.format(path), file=sys.stderr)

    if not all_exist:
        return 1

    return 0


def run_flake8(paths):
    if flake8_main is None:
        return 0

    print('Running flake8 code linting')
    exit_code = 0   # flake8 < 3 path - 3+ always raises SystemExit
    try:
        original_argv = sys.argv
        sys.argv = ['flake8'] + paths
        flake8_main()
    except SystemExit as e:
        exit_code = e.code
    finally:
        sys.argv = original_argv

    print('flake8 failed' if exit_code else 'flake8 passed')
    return exit_code


def run_modernize(paths):
    if libmodernize_main is None:
        return 0

    print('Running modernize checks')
    try:
        orig_stdout = getattr(sys, 'stdout')
        out = StringIO()
        setattr(sys, 'stdout', out)
        libmodernize_main(paths)
    finally:
        sys.stdout = orig_stdout
    output = out.getvalue()
    print(output)
    ret = len(output)
    print('modernize failed' if ret else 'modernize passed')
    return ret


def run_isort(paths):
    if isort_main is None:
        return 0

    print('Running isort check')
    original_argv = sys.argv
    sys.argv = ['isort', '--recursive', '--check-only', '--diff'] + paths
    try:
        isort_main()
        return 0
    except SystemExit as e:
        return e.code
    finally:
        sys.argv = original_argv


def run_setup_py_check():
    print('Running setup.py check')
    return subprocess.call([
        'python', 'setup.py', 'check',
        '-s', '--restructuredtext', '--metadata'
    ])
