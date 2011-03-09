#!/usr/bin/env python
from api import Filter
import lxml.html
class AfterString(Filter):
    '''
    Discards all content after and including a specified string.
    '''
    def __init__(self, string):
        self.string = string

    def filter(self, input):
        index = input.find(self.string)
        if index:
            return input[:index]
        else:
            return input

class HTMLAfterString(AfterString):
    '''
    Like AfterString, but is HTML-aware.
    '''
    def filter(self, input):
        doc = lxml.html.fromstring(input)
        delete = False
        for node in doc.getiterator():
            if delete:
                node.getparent().remove(node)
            try:
                index = node.text.find(self.string)
                if index:
                    node.text = node.text[:index]
                    delete = True
            except AttributeError:
                pass
        return lxml.html.tostring(doc)

class HTMLIds(Filter):
    '''
    Discards ID attributes of all elements.
    '''
    def filter(self, input):
        doc = lxml.html.fromstring(input)
        for node in doc.getiterator():
            try:
                del node.attrib['id']
            except:
                pass
        return lxml.html.tostring(doc)


