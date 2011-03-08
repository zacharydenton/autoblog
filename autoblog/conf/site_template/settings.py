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
    filters.rewrite.GoogleTranslateFilter('es', 'en', percentage=0.3),
]

SITE_DIR = os.path.abspath(os.path.dirname(__file__))
POST_DIR = os.path.join(SITE_DIR, '_posts')
TEMPLATES = jinja2.Environment(loader=jinja2.PackageLoader('autoblog', 'templates'))
