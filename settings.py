#!/usr/bin/env python
import os
import sources
import filters
import jinja2

DEBUG = True

feed_urls = [
    'http://wordpress.org/news/feed/',
]

SOURCES = [
    sources.rss.RssSource(feed_urls),
]

FILTERS = [
    filters.seo.NoFollow(),
    filters.rewrite.GoogleTranslateFilter('sv', 'en', percentage=0.3),
    #filters.discard.AfterString('Buy now!')
]

SITE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'site')
POST_DIR = os.path.join(SITE_DIR, '_posts')
TEMPLATES = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
