taiga-print-report
==================

|License|

A simple script to extract an HTML report from a Taiga project.


Istallation
-----------

::

    pip install git+https://github.com/morlandi/taiga-print-report


Config file
-----------

A sample config file "~/.taiga_print_report.conf" is automatically created on first run.

You should edit it to supply appropriate credentials.

::

    [general]
    host=HOST
    username=USERNAME
    password=PASSWORD
    copyright=YOUR COPYRIGHT HERE ...


Usage
-----

::

    $ taiga_print_report  --help

    Using config file "/Users/YOU/.taiga_print_report.conf"
    usage: taiga_print_report [-h] [--host HOST] [--username USERNAME]
                              [--password PASSWORD] [--copyright COPYRIGHT]
                              [--project PROJECT] [--summary] [--group-by-epics]
                              [--wiki]

    Extract printable report from Taiga Project

    optional arguments:
      -h, --help            show this help message and exit
      --host HOST           if specified, overrides configured value
      --username USERNAME   if specified, overrides configured value
      --password PASSWORD   if specified, overrides configured value
      --copyright COPYRIGHT
                            if specified, overrides configured value
      --project PROJECT
      --summary, -s         Export CSV summary instead of HTML document
      --group-by-epics, -e  Group user stories by epic (default is by Milestones)
      --wiki, -w            Print wiki pages


Sample usages
-------------

List all projects::

    $ taiga_print_report

    Using config file "/Users/morlandi/.taiga_print_report.conf"
    Available Projects:
    [  12] morlandi-testkanban "TestKanban"
    [  13] morlandi-testscrum "TestScrum"
    ...

Extract a detailed HTML report for given project::

    $ taiga_print_report --project=12 > project_by_milestones.html

Same, but grouped by epics::

    $ taiga_print_report --project=12 --group-by-epics > project_by_epics.html

Extract a summary of User Stories::

    $ taiga_print_report --project=12 --summary > project_summary.csv

Print project's wiki::

    $ taiga_print_report --project=12 --wiki > project_wiki.html



.. |License| image:: https://img.shields.io/github/license/nephila/python-taiga.svg?style=flat-square
   :target: https://pypi.python.org/pypi/python-taiga/
    :alt: License

Credits
-------

- `python-taiga: A module for using the Taiga REST API <https://github.com/nephila/python-taiga/>`_

Notes
-----

Tested with Python 3.6.

At this moment requires a customized version of python-taiga,
which adds the capability to extract project's Epics::

    pip install git+https://github.com/morlandi/python-taiga.git

I'm willing to send a PR asap to fix this.



.. |License| image:: https://img.shields.io/github/license/nephila/python-taiga.svg?style=flat-square
   :target: https://pypi.python.org/pypi/python-taiga/
    :alt: License
