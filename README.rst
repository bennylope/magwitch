========
Magwitch
========

A little tool built on top of `pip` for understanding Python package
dependencies.

.. image:: docs/pip-magwitch.jpg

While I have a great expectations for what this project will do, it is pretty
basic to start with - by design - and very much in flux.

Installation
============

Download source and run::

    python setup.py install

Usage
=====

Magwitch uses the script name `abel`.

requires
--------

See what other packages a given package depends on.::

    $ abel requires sphinx
    snowballstemmber
    six
    alabaster
    docutils
    jinja2
    pygments
    sphinx-rtd-theme
    babel

Options
~~~~~~~

    `--full`
        Produce a list recursively of packages required by the original
        package.

    `--tree`
        An output flat for generating a `full` list as a tree of requirements.

required_by
-----------

See what other packages require the given package.::

    $ abel required_by sphinx
    sphinx-rtd-theme

Options
~~~~~~~

    `--full`
        Produce a list recursively of packages dependent on the original
        package.

    `--tree`
        An output flat for generating a `full` list as a tree of requirements.
