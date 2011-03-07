#!/usr/bin/env python
import sources
import filters

feed_urls = [
    'http://wordpress.org/news/feed/',
]

SOURCES = [
    sources.rss.RssSource(feed_urls),
]

FILTERS = [
    filters.seo.SeoFilter(),
    filters.rewrite.GoogleTranslateFilter(),
]
