#!/usr/bin/env python
'''
A generic RSS Feed content source.
'''
from api import ContentSource, Content
import datetime
import feedparser
import pprint

class RssSource(ContentSource):
    def __init__(self, feed_urls):
        self.feed_urls = feed_urls

    def get_posts(self):
        for feed_url in self.feed_urls:
            doc = feedparser.parse(feed_url)
            for e in doc.entries:
                try:
                    yield Content(
                        title=e.title,
                        content=e.content[0].value,
                        time=e.date_parsed,
                    )
                except Exception as e:
                    print e


