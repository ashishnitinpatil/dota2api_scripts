#!/usr/bin/env python
"""
=================
 dota2api_scripts
=================

dota2api_scripts contains scripts to fetch Dota2 API data

Installation
============

Install via pip::

    $ pip install git+https://github.com/ashishnitinpatil/dota2api_scripts.git

or, download repository zip and manually install by::

    $ python setup.py install

"""

from distutils.core import setup

setup(
    name='dota2api_scripts',
    version='0.1.0',
    description='Python tools for Dota 2 API',
    long_description=__doc__,
    author='Ashish Nitin Patil',
    author_email="ashishnitinpatil@gmail.com",
    download_url="https://github.com/ashishnitinpatil/dota2api_scripts",
    url='https://github.com/ashishnitinpatil/dota2api_scripts',
    packages=['dota2api_scripts'],
    # package_data={"dota2api_scripts": ["data/*.json"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: New BSD License",
        "Topic :: Games/Entertainment",
    ]
)
