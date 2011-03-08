#!/usr/bin/env python
from autoblog import lib

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

def main():
    posts = lib.syndicate_content()
    lib.save_content(posts)

if __name__ == "__main__":
    main()

