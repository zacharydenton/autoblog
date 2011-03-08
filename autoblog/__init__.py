#!/usr/bin/env python

# metadata
__author__ = 'Zach Denton'
__author_email__ = 'zacharydenton@gmail.com'
__version__ = '0.2'
__url__ = 'http://zacharydenton.com/code/autoblog/'
__longdescr__ = '''
Autoblogging software written in Python. Syndicated content,
sends the content through a series of filters, and outputs
in a format that Jekyll can understand.
'''
__classifiers__ = [
    'Topic :: Text Processing'
]

import conf; from conf import *
import filters; from filters import *
import sources; from sources import *
