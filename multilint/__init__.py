from __future__ import absolute_import, print_function

import argparse
import io
import os
import subprocess
import sys
from configparser import SafeConfigParser

try:
    # Skipping patched_main since we shouldn't need the two patches it applies.
    # At time of writing, these are multiprocessing.freeze_support() and
    # forcing click to accept non-ASCII file paths
    from black import main as black_main
except ImportError:
    black_main = None

try:
    from flake8.main.cli import main as flake8_main
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

__author__ = "Adam Johnson"
__email__ = "me@adamj.eu"
__version__ = "3.0.0"


def main():
    sys.exit(run(sys.argv[1:]))


parser = argparse.ArgumentParser(description="Run multiple python linters easily")
parser.add_argument(
    "paths",
    metavar="PATH",
    type=str,
    nargs="*",
    help="Path(s) that override the `paths` settings.",
)
parser.add_argument(
    "--skip",
    dest="skip",
    type=str,
    action="append",
    help="Name(s) of linters that are installed but should be skipped.",
    choices=["flake8", "modernize", "isort", "setup.py"],
)


def run(raw_args):
    settings = load_settings()

    args = parser.parse_args(raw_args)
    skip = args.skip or ()
    paths = list(args.paths)

    if not paths:
        paths = settings["paths"]

    ret = check_paths(paths)
    if ret:
        return ret

    if "black" not in skip:
        ret = run_black(paths)
        if ret:
            return ret

    if "flake8" not in skip:
        ret = run_flake8(paths)
        if ret:
            return ret

    if "modernize" not in skip:
        ret = run_modernize(paths)
        if ret:
            return ret

    if "isort" not in skip:
        ret = run_isort(paths)
        if ret:
            return ret

    # Broken on 2.7.9 due to http://bugs.python.org/issue23063
    if sys.version_info[:3] != (2, 7, 9):
        if "setup.py" not in skip:
            ret = run_setup_py_check(paths)
            if ret:
                return ret

    return 0


MAX_CONFIG_SEARCH_DEPTH = 25
default_settings = {"paths": []}


def load_settings():
    settings = default_settings.copy()
    _update_settings_from_file("setup.cfg", settings)
    return settings


def _update_settings_from_file(section, settings):
    tries = 0
    current_directory = os.path.normpath(os.getcwd())
    config_file = None
    while current_directory and tries < MAX_CONFIG_SEARCH_DEPTH:
        potential_path = os.path.join(current_directory, "setup.cfg")
        if os.path.exists(potential_path):
            config_file = potential_path
            break

        new_directory = os.path.split(current_directory)[0]
        if current_directory == new_directory:
            break
        current_directory = new_directory
        tries += 1

    if config_file and os.path.exists(config_file):
        with open(config_file, "rU") as fp:
            config = SafeConfigParser()
            config.readfp(fp)
        if config.has_section("tool:multilint"):
            settings.update(sanitize(config.items("tool:multilint")))


def sanitize(config_items):
    output = {}
    for key, value in dict(config_items).items():
        if key in default_settings:
            if isinstance(default_settings[key], list):
                value = [v.strip() for v in value.split("\n") if v.strip()]
            output[key] = value
    return output


def check_paths(paths):
    if not paths:
        sys.stderr.writelines(
            [
                "No paths defined in [tool:multilint] section in setup.cfg",
                "nor passed as arguments to the multilint command",
            ]
        )
        return 1

    all_exist = True
    for path in paths:
        if not os.path.exists(path):
            all_exist = False
            sys.stderr.writelines(["Path {} does not exist".format(path)])

    if not all_exist:
        return 1

    return 0


def run_black(paths):
    if black_main is None:
        return 0

    print("Running black check")
    exit_code = 0
    try:
        black_main(["--check"] + paths)
    except SystemExit as exc:
        exit_code = exc.code

    if exit_code:
        print("black failed")
    else:
        print("black passed")
    return exit_code


def run_flake8(paths):
    if flake8_main is None:
        return 0

    print("Running flake8 code linting")
    try:
        original_argv = sys.argv
        sys.argv = ["flake8"] + paths
        flake8_main()
    except SystemExit as e:  # Always raised
        exit_code = e.code
        sys.argv = original_argv

    if exit_code:
        print("flake8 failed")
    else:
        print("flake8 passed")
    return int(exit_code)


def run_modernize(paths):
    if libmodernize_main is None:
        return 0

    print("Running modernize checks")
    try:
        orig_stdout = getattr(sys, "stdout")
        out = io.StringIO()
        setattr(sys, "stdout", out)
        ret = libmodernize_main(paths)
    finally:
        sys.stdout = orig_stdout
    output = out.getvalue()
    print(output)

    has_patch_lines = any(
        line.startswith(("+++", "---")) for line in output.splitlines()
    )
    if has_patch_lines or ret != 0:
        print("modernize failed")
        return max(ret, 1)
    print("modernize passed")
    return 0


def run_isort(paths):
    if isort_main is None:
        return 0

    print("Running isort check")
    original_argv = sys.argv
    sys.argv = ["isort", "--recursive", "--check-only", "--diff"] + paths
    try:
        isort_main()
        return 0
    except SystemExit as e:
        return e.code
    finally:
        sys.argv = original_argv


def run_setup_py_check(paths):
    if "setup.py" not in paths:
        return 0
    print("Running setup.py check")
    return subprocess.call(
        ["python", "setup.py", "check", "-s", "--restructuredtext", "--metadata"]
    )
