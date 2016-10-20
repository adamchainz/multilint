=======
History
=======

Pending
-------

* New notes here

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
