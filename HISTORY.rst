=======
History
=======

Pending
-------

* New notes here

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
