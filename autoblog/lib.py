#!/usr/bin/env python
import os
import json
import urllib
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
            post.content = filter.filter(post.content)

    return posts

def save_content(posts):
    post_template = settings.TEMPLATES.get_template('post.html')
    for post in posts:
        output = get_filename(post)
        if not os.path.isdir(settings.POST_DIR):
            os.mkdir(settings.POST_DIR)
        open(output, 'w').write(post_template.render(post=post).encode('utf-8'))

def find_feeds(keyphrase):
    '''
    Search for feeds matching a keyphrase.
    '''
    query = urllib.urlencode({'v': '1.0', 'q': keyphrase})
    url = "http://ajax.googleapis.com/ajax/services/search/web?" + query
    results_page = urllib.urlopen(url)
    results = json.loads(results_page.read())
    
    return [result['url'] for result in results['responseData']['results']]
