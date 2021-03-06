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
Classes for structuring the package environment and building dependency
relationships.
"""

try:
    from collections import UserDict
except ImportError:
    from UserDict import IterableUserDict as UserDict


class Environment(UserDict):
    """
    Matrix representation of the environment and installed packages.
    """
    def __init__(self, working_set, **kwargs):
        """
        `installed` is the domain of the installed package environment.
        """
        self.installed = set([req.key for req in working_set])
        self.data = {
            package.key: {
                req.key: req.specs for req in package.requires()
            } for package in working_set
        }

    def requires(self, package_key):
        """
        Returns an iterable of package keys (strings) indicating which packages
        upon which the given package *directly* depends.

        $ magwitch requires sphinx
        alabaster
        pygments
        sphinx-rtd-theme
        babel
        jinja2
        snowballstemmer
        six
        docutils
        """
        return list(self.data.get(package_key, {}).keys())

    def required_by(self, package_key):
        """
        Show which packages directly depend on the given package

        $ magwich requiredby jinja2
        sphinx
        """
        for key, packages in self.data.items():
            if package_key in packages.keys():
                yield key

    def requires_full(self, package_key, installed=set()):
        """
        Returns the full list of packages required by the one mentioned

        Ideally this would be a tree. The tree may _show_ duplicates but it
        will not build out the branches for a given node more than once.

        In the event that there is a dependency cycle (in the case of a tree,
        specific only to the branch) then that branch of requirement checking
        should end.

        Command line examples:

        $ magwitch requires mypackage
        dependency-one
        dependency-two

        $ magwitch requires mypackage --full
        dependency-one
        sub-dependency
        dependency-two
        sub-dependency-three
        another-sub
        yet-another

        $ magwitch requires mypackage --full --tree
        dependency-one
            sub-dependency
        dependency-two
            sub-dependency-three
            another-sub
                yet-another

        """
        # First ensure the package we're checking is saved away. If there's any
        # kind of cyclic dependency this could otherwise lead to a recursive
        # runtime error.
        installed = installed.union(package_key)

        requires = self.requires(package_key)  # list of pkg keys
        if not requires:
            return requires  # return if empty

        dependencies = []

        for req in requires:
            if req in installed:
                continue
            installed.add(req)
            dependencies.append((req, self.requires_full(req, installed)))

        return dependencies

    def required_by_full(self, package_key, installed=set()):
        """
        """
        installed = installed.union(package_key)

        required_by = self.required_by(package_key)  # list of pkg keys

        if not required_by:
            return required_by

        depends = []

        for req in required_by:
            if req in installed:
                continue
            installed.add(req)
            depends.append((req, self.required_by_full(req, installed)))

        return depends
