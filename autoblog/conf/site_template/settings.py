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
    autoblog.filters.discard.HTMLIds(),
    autoblog.filters.discard.AfterString('<p>No related posts.</p>'),
    autoblog.filters.discard.AfterString('<div class="blogger-post-footer">'),
    autoblog.filters.discard.AfterString('<p>Related posts:</p>'),
    autoblog.filters.discard.AfterString('<strong>Author:</strong>'),
    autoblog.filters.discard.AfterString('Filed under:'),
    autoblog.filters.misc.ValidHTML(),
]

SITE_DIR = os.path.abspath(os.path.dirname(__file__))
POST_DIR = os.path.join(SITE_DIR, '_posts')
BUILD_DIR = os.path.join(SITE_DIR, '_site')
TEMPLATES = jinja2.Environment(loader=jinja2.PackageLoader('autoblog', 'templates'))
REMOTE = 'CHANGEME@CHANGEME:CHANGEME/'
FEED_URL='http://CHANGEME/atom.xml'
