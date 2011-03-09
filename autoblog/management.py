#!/usr/bin/env python
import argparse
import autoblog
import subprocess
import os
import sys

try:
    import settings
    import lib
except ImportError:
    pass

def execute_from_command_line():
    parser = argparse.ArgumentParser(description='Automatically compile content from RSS feeds into a single blog.')
    subparsers = parser.add_subparsers()

    # init command
    parser_init = subparsers.add_parser('init', help='Initialize a new autoblog')
    parser_init.add_argument('sitename', help='a name for the new autoblog')
    parser_init.set_defaults(func=init)

    # update command
    parser_update = subparsers.add_parser('update', help='Update the autoblog')
    parser_update.set_defaults(func=update)

    # build command
    parser_build = subparsers.add_parser('build', help='build the autoblog')
    parser_build.set_defaults(func=build)

    # deploy command
    parser_deploy = subparsers.add_parser('deploy', help='deploy the autoblog to server')
    parser_deploy.set_defaults(func=deploy)

    # sync command
    parser_sync = subparsers.add_parser('sync', help='update -> build -> deploy')
    parser_sync.set_defaults(func=sync)

    # scour command
    parser_scour = subparsers.add_parser('scour', help='Given a keyphrase, scour the internet for suitable content feeds')
    parser_scour.add_argument('phrase', help='the keyphrase to search for')
    parser_scour.set_defaults(func=scour)

    args = parser.parse_args()
    args.func(args)

def execute_manager(settings_mod):
    setup_environ(settings_mod)
    execute_from_command_line()

def setup_environ(settings_mod, original_settings_path=None):
    """
    Configures the runtime environment. This can also be used by external
    scripts wanting to set up a similar environment to manage.py.
    Returns the project directory (assuming the passed settings module is
    directly in the project directory).

    The "original_settings_path" parameter is optional, but recommended, since
    trying to work out the original path from the module can be problematic.
    """
    # Add this project to sys.path so that it's importable in the conventional
    # way. For example, if this file (manage.py) lives in a directory
    # "myproject", this code would add "/path/to/myproject" to sys.path.
    if '__init__.py' in settings_mod.__file__:
        p = os.path.dirname(settings_mod.__file__)
    else:
        p = settings_mod.__file__
    project_directory, settings_filename = os.path.split(p)
    if project_directory == os.curdir or not project_directory:
        project_directory = os.getcwd()
    project_name = os.path.basename(project_directory)

    # Strip filename suffix to get the module name.
    settings_name = os.path.splitext(settings_filename)[0]

    # Strip $py for Jython compiled files (like settings$py.class)
    if settings_name.endswith("$py"):
        settings_name = settings_name[:-3]

    # Set AUTOBLOG_SETTINGS_MODULE appropriately.
    if original_settings_path:
        os.environ['AUTOBLOG_SETTINGS_MODULE'] = original_settings_path
    else:
        os.environ['AUTOBLOG_SETTINGS_MODULE'] = '%s.%s' % (project_name, settings_name)

    # Import the project module. We add the parent directory to PYTHONPATH to
    # avoid some of the path errors new users can have.
    sys.path.append(os.path.join(project_directory, os.pardir))
    sys.path.pop()

    return project_directory

def copy_helper(name, directory):
    """
    Copies either a Django application layout template or a Django project
    layout template into the specified directory.

    """
    # name -- The name of the application or project.
    # directory -- The directory to which the layout template should be copied.
    import re
    import shutil
    if not re.search(r'^[_a-zA-Z]\w*$', name): # If it's not a valid directory name.
        # Provide a smart error message, depending on the error.
        if not re.search(r'^[_a-zA-Z]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters and underscores'
        raise CommandError("%r is not a valid name. Please %s." % (name, message))
    top_dir = os.path.join(directory, name)
    os.mkdir(top_dir)

    # Determine where the app or project templates are. Use
    # django.__path__[0] because we don't know into which directory
    # django has been installed.
    template_dir = os.path.join(autoblog.__path__[0], 'conf', 'site_template')

    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir)+1:].replace('site_name', name)
        if relative_dir:
            os.mkdir(os.path.join(top_dir, relative_dir))
        for subdir in subdirs[:]:
            if subdir.startswith('.'):
                subdirs.remove(subdir)
        for f in files:
            path_old = os.path.join(d, f)
            path_new = os.path.join(top_dir, relative_dir, f.replace('site_name', name))
            fp_old = open(path_old, 'r')
            fp_new = open(path_new, 'w')
            fp_new.write(fp_old.read().replace('{{ site_name }}', name))
            fp_old.close()
            fp_new.close()
            try:
                shutil.copymode(path_old, path_new)
                _make_writeable(path_new)
            except OSError:
                sys.stderr.write(style.NOTICE("Notice: Couldn't set permission bits on %s. You're probably using an uncommon filesystem setup. No problem.\n" % path_new))

def _make_writeable(filename):
    """
    Make sure that the file is writeable. Useful if our source is
    read-only.

    """
    import stat
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

def init(args):
    directory = os.getcwd()
    name = args.sitename
    copy_helper(name, directory)

def update(args):
    posts = lib.syndicate_content()
    lib.save_content(posts)

def scour(args):
    feeds = lib.find_feeds(args.phrase)
    for feed in feeds:
        print feed

def deploy(args):
    local = settings.BUILD_DIR
    if not local.endswith('/'):
        local += '/'
    remote = settings.REMOTE
    if not remote.endswith('/'):
        remote += '/'
    subprocess.call(['rsync', '-rtz', local, remote])

def build(args):
    os.chdir(settings.SITE_DIR)
    subprocess.call('jekyll')

def sync(args):
    update(args)
    build(args)
    deploy(args)
