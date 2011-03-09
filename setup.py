#!/usr/bin/env python
'''
Installer script for autoblog.
'''
from setuptools import setup, find_packages
import os
import autoblog

setup (
    name = "autoblog",
    description = "A minimalistic autoblog which adheres to Unix principles.",
    author = autoblog.__author__,
    author_email = autoblog.__author_email__,
    version = autoblog.__version__,
    url = autoblog.__url__,
    long_description = autoblog.__longdescr__,
    classifiers = autoblog.__classifiers__,
    packages = find_packages(),
    include_package_data=True,
    scripts = ['autoblog-admin.py'],
    install_requires = [
        'nltk',
        'jinja2',
        'lxml',
        'BeautifulSoup',
    ]
)
