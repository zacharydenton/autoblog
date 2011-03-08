#!/usr/bin/env python
import os
import subprocess

import settings
from sources.lib import html2markdown

def get_filename(post):
    basename = '%s-%s.html' % (post.time.strftime('%Y-%m-%d'), post.slug)
    filename = os.path.join(settings.POST_DIR, basename)
    return filename

def syndicate_content():
    posts = []
    for source in settings.SOURCES:
        posts += source.get_posts()

    for post in posts:
        if settings.DEBUG:
            print 'filtering %s' % post.title
        for content_filter in settings.FILTERS:
            post.content = content_filter.filter(post.content)

    return posts

def save_content(posts):
    post_template = settings.TEMPLATES.get_template('post.html')
    for post in posts:
        output = get_filename(post)
        if settings.DEBUG:
            print 'saving %s' % output
        if not os.path.isdir(settings.POST_DIR):
            os.mkdir(settings.POST_DIR)
        open(output, 'w').write(post_template.render(post=post).encode('utf-8'))
