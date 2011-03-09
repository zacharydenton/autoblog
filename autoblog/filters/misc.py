#!/usr/bin/env python
from api import Filter
import subprocess
import lxml.html

class UnixFilter(Filter):
    '''
    Pipes the content through an arbitrary Unix filter.
    '''
    def __init__(self, command):
        self.command = command

    def filter(self, input):
        p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        return p.communicate(input=input)[0]

class CleanHTML(Filter):
    '''
    Applies the lxml.html.clean_html function to the input.
    '''
    def filter(self, input):
        return lxml.html.clean_html(input)

class ValidHTML(Filter):
    '''
    Takes any HTML, and returns valid HTML.
    '''
    def filter(self, input):
        return lxml.html.tostring(lxml.html.html5parser.fromstring(input))
