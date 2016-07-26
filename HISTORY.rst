=======
History
=======

Pending
-------

* New notes here

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
