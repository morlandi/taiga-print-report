taiga-print-report
==================

|License|

A simple script to extract an HTML report from a Taiga project.


Sample usages
-------------

List all projects::

    taiga-print-report.py HOST username password

Extract a detailed HTML report for given project::

    taiga-print-report.py HOST username password --project=1 --copyright="Acme"

Extract a summary of User Stories::

    taiga-print-report.py HOST username password --project=1 --summary


.. |License| image:: https://img.shields.io/github/license/nephila/python-taiga.svg?style=flat-square
   :target: https://pypi.python.org/pypi/python-taiga/
    :alt: License

Credits
-------

- `python-taiga: A module for using the Taiga REST API <https://github.com/nephila/python-taiga/>`_

Notes
-----

Tested with Python 3.6.

At this moment requires a customized version of python-taiga (https://github.com/morlandi/taiga-print-report),
which adds the capability to extract project's Epics::

    pip install git+https://github.com/morlandi/python-taiga.git

I'm willing to send a PR asap to fix this.



.. |License| image:: https://img.shields.io/github/license/nephila/python-taiga.svg?style=flat-square
   :target: https://pypi.python.org/pypi/python-taiga/
    :alt: License
