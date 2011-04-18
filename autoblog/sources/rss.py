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
            print "processing %s" % feed_url
            doc = feedparser.parse(feed_url)
            source = doc.feed.link
            for e in doc.entries:
                url = e.link
                try:
                    yield Content(
                        title=e.title,
                        content=e.content[0].value,
                        time=datetime.datetime(*e.date_parsed[:6]),
                        source=source,
                        url=url,
                    )
                except Exception as e:
                    pass



