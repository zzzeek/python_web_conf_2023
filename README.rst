===========================
SQLAlchemy 2.0 - Let's Talk
===========================

This package is the full source code for the **SQLAlchemy 2.0 - Let's Talk**
Tutorial.

The main thing participants will be interested in is to walk through the
interactive code demonstrations, which are present here in the
./slides/ folder.

**note:  You don't have to install the software in order to participate in the
tutorial!  Mike will be running through the same code in the screenshare.**

The .py files in this folder are plain Python files and can be read directly
as the code is presented.  Alternatively, they can be run within the same
"slide runner" environment as follows (prerequisites: git, Python virtualenv
are installed):

Installation
------------

1. Dependencies::

    python 3.7 or higher (3.10 or 3.11 preferred)
    git
    pip
    virtualenv

2. Install using virtualenv and pip::

    $ git clone https://github.com/zzzeek/python_web_conf_2023
    $ cd python_web_conf_2023
    $ virtualenv .venv
    $ source .venv/bin/activate
    $ pip install .

3. Run slides::

    sliderepl 01_engine_usage.py

    sliderepl 02_metadata.py

    # ... etc


The source .rst for the presentation itself is in ./presentation/.
