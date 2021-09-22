rmq-definitions
===============
*Deterministically sort and format RabbitMQ definition backups*

``rmq-definitions`` is an application that provides deterministic sorting and
formatting of JSON based RabbitMQ definition backups.  By transforming the JSON
definitions file provided by the RabbitMQ Management UI, differential backups
of RabbitMQ's definitions can be made.

Want to know when a certain queue was added or a binding was removed? You can
use ``rmq-definitions`` as part of a cron job that writes out the definitions
to a git repository and commits any changes to git, pushing to a remote
location. By doing so, definition differences between commits can be
clearly tracked.

|Version| |Status| |Coverage| |License|

Requirements
------------
``rmq-definitions`` requires Python 2.7, 3.4, 3.5, 3.6, 3.7, 3.8, or 3.9, and
`requests <http://docs.python-requests.org/en/master/>`_.

Installation
------------
``rmq-definitions`` is available on the Python package index and is
installable via pip:

.. code:: bash

    pip install rmq-definitions

Usage
-----

.. code::

	usage: rmq-sorted-definitions [-h] [--url URL] [-u USERNAME] [-p PASSWORD]
	                              [DESTINATION]

	Deterministically sort and format RabbitMQ definition backups

	positional arguments:
	  DESTINATION           Location to write the definitions to. Default: STDOUT

	optional arguments:
	  -h, --help            show this help message and exit
	  --url URL             The RabbitMQ Management API base URL. Default:
	                        http://localhost:15672
	  -u USERNAME, --username USERNAME
	                        The RabbitMQ Management API username. Default: guest
	  -p PASSWORD, --password PASSWORD
	                        The RabbitMQ Management API password. Default: guest
	  -f FROM_FILE, --from-file FROM_FILE
	                        Read definitions from a file instead of the Management
	                        API


.. |Version| image:: https://img.shields.io/pypi/v/rmq-definitions.svg?
   :target: http://badge.fury.io/py/rmq-definitions

.. |Status| image:: https://img.shields.io/travis/gmr/rmq-definitions.svg?
   :target: https://travis-ci.org/gmr/rmq-definitions

.. |Coverage| image:: https://img.shields.io/codecov/c/github/gmr/rmq-definitions.svg?
   :target: https://codecov.io/github/gmr/rmq-definitions?branch=master

.. |License| image:: https://img.shields.io/pypi/l/rmq-definitions.svg?
   :target: https://rmq-definitions.readthedocs.org
