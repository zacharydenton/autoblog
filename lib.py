#!/usr/bin/env python
import os
import subprocess
from jinja import from_string

import settings
from sources.lib import html2markdown

def syndicate_content():
    posts = []
    for source in settings.SOURCES:
        posts += source.get_posts()

    for item in posts:
        for content_filter in settings.FILTERS:
            item.content = content_filter.filter(item.content)

    return posts

post_template = from_string('''\
---
layout: post
title: '{{ post.title }}'
tags:
{% for tag in post.tags %}
- '{{ tag }}'
{% endfor %}
categories: 
{% for category in post.categories %}
- '{{ category }}'
{% endfor %}
excerpt: '{{ post.excerpt }}'
---
{{ post.content }}
''')

def save_content(posts):
    for post in posts:
        filename = '%s-%s.html' % (post.time.strftime('%Y-%m-%d'), post.slug)
        output = os.path.join(settings.POST_DIR, filename)
        if not os.path.isdir(settings.POST_DIR):
            os.mkdir(settings.POST_DIR)
        open(output, 'w').write(post_template.render(post=post).encode('utf-8'))

def regenerate_site():
    os.chdir(settings.SITE_DIR)
    subprocess.call('jekyll')
