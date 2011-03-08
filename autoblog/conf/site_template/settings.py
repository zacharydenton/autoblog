#!/usr/bin/env python
import os
import autoblog
import jinja2

DEBUG = True

feed_urls = [
    'http://wordpress.org/news/feed/',
]

SOURCES = [
    autoblog.sources.rss.RssSource(feed_urls),
]

FILTERS = [
    autoblog.filters.seo.NoFollow(),
    autoblog.filters.rewrite.GoogleTranslateFilter('es', 'en', percentage=0.3),
]

SITE_DIR = os.path.abspath(os.path.dirname(__file__))
POST_DIR = os.path.join(SITE_DIR, '_posts')
TEMPLATES = jinja2.Environment(loader=jinja2.PackageLoader('autoblog', 'templates'))
