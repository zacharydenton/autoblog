#!/usr/bin/env python
import settings

def syndicate_content():
    posts = []
    for source in settings.SOURCES:
        posts += source.get_posts()

    for item in posts:
        for content_filter in settings.FILTERS:
            item.content = content_filter.filter(item.content)

    return posts

def save_content(posts):
    pass

def regenerate_site():
    pass
