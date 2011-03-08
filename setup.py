#!/usr/bin/env python
'''
Installer script for autoblog.
'''

from distutils.core import setup
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
    packages = ['autoblog',
                'autoblog.sources',
                'autoblog.filters',
                'autoblog.templates',
               ],
    scripts = ['autoblog-admin.py'],
    requires = ['nltk']
)
