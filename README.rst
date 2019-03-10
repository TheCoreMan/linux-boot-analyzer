===================
Linux Boot Analyzer
===================


.. image:: https://img.shields.io/pypi/v/linux_boot_analyzer.svg
        :target: https://pypi.python.org/pypi/linux_boot_analyzer

.. image:: https://img.shields.io/travis/TheCoreMan/linux-boot-analyzer.svg
        :target: https://travis-ci.org/TheCoreMan/linux-boot-analyzer

.. image:: https://readthedocs.org/projects/linux-boot-analyzer/badge/?version=latest
        :target: https://linux-boot-analyzer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/TheCoreMan/linux-boot-analyzer/shield.svg
     :target: https://pyup.io/repos/github/TheCoreMan/linux-boot-analyzer/
     :alt: Updates



A program for analyzing Linux startup units and their traits, with a backend server for storing and querying the results.


* Free software: MIT license
* Documentation: https://linux-boot-analyzer.readthedocs.io.


Overview
--------
The collector
^^^^^^^^^^^^^
The collector is the part which runs on the target machine and actually collects the data from the client.

It needs *python 3* and has no external dependencies. This is by design - so if a pull request adds external
dependencies it will be automatically rejected. This program is meant to run on Linux .

To see it's usage run `collector.py -h`. At the time of writing:

::

    ssh://dude500@34.76.30.202:22/usr/bin/python3 -u /tmp/pycharm_project_410/linux_boot_analyzer/collector/collector.py -h
    usage: collector.py [-h] {print,file} ...

    Analyze linux boot unit files. Run me on the machine which you want to analyze!

    optional arguments:
      -h, --help    show this help message and exit

    output:
      {print,file}  Choose where to output the result to
        print       Print to standard output (useful for debugging).
        file        Write to local file.

The server
^^^^^^^^^^
Well, it ought to get POST requests from the clients and push them into our DB. Hasn't been tested in prod yet, so
hasn't been developed properly yet.

To run it:
1) Create a secret.ini file with a password key in the postgres section, like this:

::

    [postgresql]
    password=PUT_DATABASE_PASSWORD_HERE

2) Run it as a flask app, like this:

::

    FLASK_APP = linux_boot_analyzer/analysis_repo/repo_server.py
    FLASK_ENV = development
    FLASK_DEBUG = 0
    In folder F:/code/guardicore/linux-boot-analyzer
    C:\Users\Shay\AppData\Local\Programs\Python\Python37\python.exe -m flask run --host 0.0.0.0 --port 80
     * Serving Flask app "linux_boot_analyzer/analysis_repo/repo_server.py"
     * Environment: development
     * Debug mode: off
     * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)

The DB
^^^^^^
Here to answer all your Business questions like "How many Machines have we run on?" or "how many different
/etc/init.d/networking files are out there??".

The DB is hosted on Google Cloud SQL (https://status.cloud.google.com/ ).

See connection details in the relevant .ini files, but you need to know the password to query it. I'll never tell ;)


Future
------
See https://github.com/TheCoreMan/linux-boot-analyzer/projects/1 for features that will be added, or not, or maybe.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
