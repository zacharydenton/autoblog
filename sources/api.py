#!/usr/bin/env python
import datetime
import lib

class ContentSource(object):
    '''
    Base class from which all content sources inherit.
    '''
    def __init__(self):
        pass

    def get_posts(self):
        raise NotImplementedError("Override this in a sub-class.")

class Content(object):
    def __init__(self, title, content, time, **kwargs):
        self.title = title
        self.content = content
        self.time = time

        for attr, val in kwargs.items():
            setattr(self, attr, val)

    @property
    def slug(self):
        return lib.slugify(self.title)

    @property
    def excerpt(self):
        return lib.summarize(self.content)
