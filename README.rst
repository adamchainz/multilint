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

How it works
------------

I like to keep my projects tidy with a standard set of linters. Running them
all turned out to be easier with a wrapper script, which I ended up
copy-pasting between them all. This project stops me needing to copy/paste,
centralizing running all these neat tools.

In order, it will is these linters are installed, and if so, run them:

* Run ``flake8``, for code quality
* Run ``isort`` in 'diff' mode, for import sorting
* Run ``modernize`` in 'diff' mode, for python 2/3 compatibility
* Run ``python setup.py check``, to ensure that your ``setup.py`` is well
  configured. This will require ``docutils``, and maybe ``Pygments`` if your
  ``long_description`` uses any code highlighting.

If any of them fail, ``multilint`` stops and dies with a non-zero exit code.
Otherwise it succeeds!

You need to configure the paths that will be linted (by default, only
``setup.py`` is linted). Put a section in your ``setup.cfg`` like:

.. code-block:: ini

    [multilint]
    paths = my_package
            tests
            setup.py

Usage with ``tox``
------------------

I normally run my tests with ``tox``. An example ``tox.ini`` to use
``multilint`` to do all your linting would be:

.. code-block:: ini

    [tox]
    envlist =
        py{27,35},
        py{27,35}-codestyle

    [testenv]
    deps = -rrequirements.txt
    commands = py.test

    [testenv:py27-codestyle]
    commands = multilint

    [testenv:py35-codestyle]
    commands = multilint

Just put ``multilint``, ``flake8``, etc. in your ``requirements.txt`` and
they'll automatically run.
