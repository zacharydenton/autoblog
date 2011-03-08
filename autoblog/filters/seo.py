#!/usr/bin/env python
from api import Filter
import lxml.html

class NoFollow(Filter):
    '''
    Makes all external links rel="nofollow".
    '''
    def filter(self, input):
        doc = lxml.html.fromstring(input)
        for a in doc.cssselect('a'):
            if a.get('href').startswith('http'):
                a.set('rel', 'nofollow')
        return lxml.html.tostring(doc)

