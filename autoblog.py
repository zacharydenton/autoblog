#!/usr/bin/env python
import lib
from pprint import pprint

def main():
    posts = lib.syndicate_content()
    lib.save_content(posts)
    lib.regenerate_site()

if __name__ == "__main__":
    main()

