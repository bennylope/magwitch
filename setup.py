#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import magwitch

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = magwitch.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='magwitch',
    version=version,
    description="""Package info.""",
    long_description=readme + '\n\n' + history,
    author='Ben Lopatin',
    author_email='ben@wellfire.co',
    url='https://github.com/bennylope/magwitch',
    packages=[
        'magwitch',
    ],
    include_package_data=True,
    install_requires=[
        'pip',
        'click',
    ],
    license="BSD",
    zip_safe=False,
    keywords='magwitch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'abel = magwitch:main',
        ],
    }
)
