#!/usr/bin/env python
import lib
from pprint import pprint

def main():
    posts = lib.syndicate_content()
    lib.save_content(posts)

if __name__ == "__main__":
    main()

