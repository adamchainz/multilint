=========
multilint
=========

.. image:: https://img.shields.io/pypi/v/multilint.svg
        :target: https://pypi.python.org/pypi/multilint

.. image:: https://img.shields.io/travis/adamchainz/multilint.svg
        :target: https://travis-ci.org/adamchainz/multilint

Run multiple python linters easily.

Installation and Usage
----------------------

Install with **pip**:

.. code-block:: sh

    pip install multilint

Run with:

.. code-block:: sh

    multilint

How It Works
------------

I like to keep my projects tidy with a standard set of linters. Running them
all turned out to be easier with a wrapper script, which I ended up
copy-pasting between them all. This project stops me needing to copy/paste,
centralizing running all these neat tools.

In order, it will check if these linters are installed, and if so, run them:

* ``flake8``, to check code quality
* ``isort``, in 'diff' mode to show where imports aren't sorted
* ``modernize``, in 'diff' mode to show where python 2/3 compatibility with
  ``six`` is missing
* ``python setup.py check``, to check your ``setup.py`` is well
  configured. This will require ``docutils``, and also ``Pygments`` if your
  ``long_description`` uses any code highlighting.

If any of them fail, ``multilint`` stops and dies with a non-zero exit code.
Otherwise it succeeds!

You need to configure the paths that will be linted (by default, only
``setup.py`` is linted). Put a section in your ``setup.cfg`` like:

.. code-block:: ini

    [tool:multilint]
    paths = my_package
            tests
            setup.py

Usage With ``tox``
------------------

I normally run my tests with ``tox``. An example ``tox.ini`` to use
``multilint`` to do your linting on both Python 2.7 and 3.5 would look like:

.. code-block:: ini

    [tox]
    envlist =
        py{27,35},
        py{27,35}-codestyle

    [testenv]
    deps = -rrequirements.txt
    commands = pytest

    [testenv:py27-codestyle]
    commands = multilint

    [testenv:py35-codestyle]
    commands = multilint

Then just put ``multilint``, plus the linters you want it to run (e.g.
``flake8``) in your ``requirements.txt``.
