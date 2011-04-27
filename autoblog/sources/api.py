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
        self.slug = lib.slugify(self.title)
        self.tags = [' '.join(tup) for tup in lib.collocations(self.content, threshold=2)][:5]

        for attr, val in kwargs.items():
            setattr(self, attr, val)

    @property
    def excerpt(self):
        return lib.summarize(self.content).strip()

    @property
    def yaml_title(self):
        return self.title.replace(':', ' -').replace('\n', ' ').strip()

    @property
    def yaml_excerpt(self):
        return self.excerpt.replace(':', ' -').replace('\n', ' ').strip()
