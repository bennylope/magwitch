"""
Copyright 2015 Ben Lopatin

Command line interface for magwitch.
"""

import sys
import click

from pip._vendor import pkg_resources
from magwitch.environ import Environment


@click.command()
@click.argument('pkg_name')
@click.option('--full/--short', default=False)
@click.option('--tree/--no-tree', default=False)
def requires(pkg_name, full, tree):
    """Show detailed dependency information for a package."""

    env = Environment(pkg_resources.working_set)
    if pkg_name not in env:
        sys.exit("'%s' is not an installed package!" % pkg_name)

    if not full:
        for pkg in env.requires(pkg_name):
            print(pkg)
        sys.exit()

    def tree_printer(tree_list, indent=""):
        for tree in tree_list:
            print("{0}- {1}".format(indent, tree[0]))
            if tree[1]:
                tree_printer(tree[1], indent + "  ")

    if tree:
        tree_printer(env.requires_full(pkg_name))


@click.command()
@click.argument('pkg_name')
@click.option('--full/--short', default=False)
@click.option('--tree/--no-tree', default=False)
def required_by(pkg_name, full, tree):
    """Show detailed dependency information for a package."""

    env = Environment(pkg_resources.working_set)
    if pkg_name not in env:
        sys.exit("'%s' is not an installed package!" % pkg_name)

    if not full:
        for pkg in env.required_by(pkg_name):
            print(pkg)
        sys.exit()

    def tree_printer(tree_list, indent=""):
        for tree in tree_list:
            print("{0}- {1}".format(indent, tree[0]))
            if tree[1]:
                tree_printer(tree[1], indent + "  ")

    if tree:
        tree_printer(env.required_by_full(pkg_name))
