#!/usr/bin/env python
import os
import json
import urllib
import autorss
import lxml.html
import feedparser
import subprocess

import settings

def get_filename(post):
    basename = '%s-%s.html' % (post.time.strftime('%Y-%m-%d'), post.slug)
    filename = os.path.join(settings.POST_DIR, basename)
    return filename

def syndicate_content():
    posts = []
    for source in settings.SOURCES:
        posts += source.get_posts()

    print "found %s posts" % len(posts)

    for post in posts:
        for filter in settings.FILTERS:
            try:
                post.content = filter.filter(post.content)
            except Exception as e:
                print e
                pass

    return posts

def save_content(posts):
    post_template = settings.TEMPLATES.get_template('post.html')
    for post in posts:
        output = get_filename(post)
        if not os.path.isdir(settings.POST_DIR):
            os.mkdir(settings.POST_DIR)
        open(output, 'w').write(post_template.render(post=post).encode('utf-8'))

def find_feeds(query):
    args = {
        'hl': 'en',
        'tbm': 'blg',
        'tbs': 'blgt:b',
        'q': query,
        'start': 0,
    }
    seen = set()
    while True:
        url = 'http://www.google.com/search?' + urllib.urlencode(args)
        doc = lxml.html.parse(url)
        for blog in doc.xpath('//cite'):
            url = 'http://' + blog.text_content().strip().split('/')[0] + '/'
            if url not in seen:
                feed = get_feed(url)
                if feed:
                    yield feed
                seen.add(url)
        args['start'] += 10

def get_feed(url):
    feed_url = autorss.getRSSLink(url)
    doc = feedparser.parse(feed_url)
    try:
        content = doc.entries[0].content[0].value
        return feed_url
    except Exception as e:
        return False

