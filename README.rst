=========
multilint
=========

.. image:: https://github.com/adamchainz/multilint/workflows/CI/badge.svg?branch=master
   :target: https://github.com/adamchainz/multilint/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/multilint.svg
   :target: https://pypi.org/project/multilint/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black

----

**Unmaintained:** I'm no longer maintaining this package because it's for
Python 2 compatibility and all other projects I've used it on are now Python 3
only. If you want to continue maintenance please contact me.

----

Run multiple python linters easily.

Installation and Usage
----------------------

Install with **pip**:

.. code-block:: sh

    python -m pip install multilint

Run with:

.. code-block:: sh

    multilint

Python 3.5 to 3.8  supported.

How It Works
------------

I like to keep my projects tidy with a standard set of linters. Running them
all turned out to be easier with a wrapper script, which I ended up
copy-pasting between them all. This project stops me needing to copy/paste,
centralizing running all these neat tools.

In order, it will check if these linters are installed, and if so, run them:

* `Black <https://pypi.org/project/black/>`_, to autoformat code
* `Flake8 <https://pypi.org/project/flake8/>`_, to check code quality
* `Isort <https://pypi.org/project/isort/>`_, in 'diff' mode to show where imports aren't sorted
* `Modernize <https://pypi.org/project/modernize/>`_, in 'diff' mode to show where python 2/3 compatibility with
  ``six`` is missing

If any of them fail, ``multilint`` stops and dies with a non-zero exit code.
Otherwise it succeeds!

You need to configure the paths that will be linted (by default, only
``setup.py`` is linted). Put a section in your ``setup.cfg`` like:

.. code-block:: ini

    [tool:multilint]
    paths = my_package
            tests
            setup.py

You can also pass the paths as arguments to ``multilint``, which will override
the ``settings``, like:

.. code-block:: sh

    multilint path/my_file.py path/folder1

**Note:** previously ``multilint`` supported running ``setup.py check`` if you
passed a ``setup.py`` file. This was removed as the command is deprecated. You
should instead use ``twine check`` as per the `python packaging documentation
<https://packaging.python.org/guides/making-a-pypi-friendly-readme#validating-restructuredtext-markup>`__.

Usage With ``tox``
------------------

I normally run my tests with ``tox``. An example ``tox.ini`` to use
``multilint`` to run your tests on Python 3.5-3.8 and do your linting on Python
3.8 would look like:

.. code-block:: ini

    [tox]
    envlist =
        py{35,36,37,38},
        py38-codestyle

    [testenv]
    deps = -rrequirements.txt
    commands = pytest

    [testenv:py38-codestyle]
    commands = multilint

Then just put ``multilint``, plus the linters you want it to run (e.g.
``flake8``) in your ``requirements.txt``.
