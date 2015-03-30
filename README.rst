========
Magwitch
========

A little tool built on top of `pip` for understanding Python package
dependencies.

.. image:: docs/pip-magwitch.jpg

While I have a great expectations for what this project will do, it is pretty
basic to start with - by design - and very much in flux.

Project goals
=============

- Show auxilliary information about a package, including not just the
  packages it requires, but its entire dependency lineage
- Show the same lineage but for packages which require a given package
- Show version specifications in a lineage, including conflicts and how wide the
  version window is (e.g. if package A requires package X between versions 1.0
  and 2.0, and package B requires package X between versions 0.9 and 1.5, then
  the specification window is 1.0 through 1.5)
- Generate a dependency graphs mapping version specification relationsips
- Generate Graphiz and image represenations of the dependency graph

Python 3 gets first class support with backwards support for Python 2.7 if it
doesn't get in the way.

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
