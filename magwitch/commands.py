# Copyright (c) 2015, Ben Lopatin
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with
# the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Command line interface for magwitch.
"""

import sys
import click

from pip._vendor import pkg_resources
from magwitch.environ import Environment


def tree_printer(tree_list, indent=""):
    for tree in tree_list:
        print("{0}- {1}".format(indent, tree[0]))
        if tree[1]:
            tree_printer(tree[1], indent + "  ")


def tree_as_set(tree_list):
    packages = set([leaf[0] for leaf in tree_list])
    if not packages:
        return packages

    for pkg in tree_list:
        packages = packages.union(tree_as_set(pkg[1]))

    return packages


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

    if tree:
        tree_printer(env.requires_full(pkg_name))
    else:
        for pkg in tree_as_set(env.requires_full(pkg_name)):
            print(pkg)


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

    if tree:
        tree_printer(env.required_by_full(pkg_name))
    else:
        for pkg in tree_as_set(env.required_by_full(pkg_name)):
            print(pkg)
