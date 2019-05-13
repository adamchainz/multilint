=======
History
=======

Pending Release
---------------

.. Modify the below with new release notes

3.0.0 (2019-05-13)
------------------

* Drop Python 2 and 3.4 support, only Python 3.5+ is supported now.
* Add support for running `Black <https://pypi.org/project/black/>`__, the
  Python code auto-formatter.
* Drop support for Flake8 < 3.0.0.

2.4.0 (2018-09-30)
------------------

* Support positional arguments for paths.

2.3.0 (2018-04-28)
------------------

* Fix for modernize 0.6.1+
* Run modernize on the multilint codebase itself, so it now requires six

2.2.1 (2018-03-08)
------------------

* Fix crash when setup.cfg doesn't exist.

2.2.0 (2017-09-19)
------------------

* Add ``--skip`` argument which can be used to skip particular linters even
  though they're installed.

2.1.0 (2017-06-02)
------------------

* Use ``entry_points`` in ``setup.py`` instead of ``scripts``
* Support ``python -m multilint``

2.0.2 (2016-12-06)
------------------

* Don't invoke ``python setup.py check`` if there is no ``setup.py``.

2.0.1 (2016-10-20)
------------------

* Remove default for `paths` in ``setup.cfg``.
* Check that paths exist before running the linters.

2.0.0 (2016-09-24)
------------------

* Use the config header ``tool:multilint`` in ``setup.cfg``, rather than
  ``multilint``, to avoid clashing with any potential ``setup.py`` commands.
  Your ``setup.cfg`` will need updating.

1.0.2 (2016-07-26)
------------------

* Work with ``flake8`` 3.0+ which changed the way its ``main`` function worked.

1.0.1 (2016-07-16)
------------------

* Fix modernize running on Python 2.
* Run ``isort`` in the same Python process rather than with ``subprocess``
* Properly gate ``flake8`` and ``isort`` so that they run only if they are
  installed.

1.0.0 (2016-06-19)
------------------

* First release on PyPI.
