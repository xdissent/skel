#!/usr/bin/env python

import os
settings = None

if 'SKEL_PYTHON_INIT' not in os.environ:
    import sys

    settings_mod = 'settings'
    settings_mod = os.environ.get('DJANGO_SETTINGS_MODULE', settings_mod)

    for arg in sys.argv:
        if arg.startswith('--settings='):
            settings_mod = arg.replace('--settings=', '')

    settings = __import__(settings_mod)
    
    try:
        cmd = os.path.join(settings.VIRTUAL_ENVIRONMENT_PATH, 'bin/python')
    except AttributeError:
        sys.stderr.write('Warning: settings module does not contain VIRTUAL_ENVIRONMENT_PATH\n')
    else:
        args = sys.argv[:]
        args.insert(0, cmd)
        env = os.environ.copy()
        env['SKEL_PYTHON_INIT'] = 'done'
        
        try:
            os.execve(cmd, args, env)
        except OSError:
            sys.stderr.write('Warning: could not execute interpreter in your virtual environment. Tried: %s\n' % cmd)

if settings is None:
    try:
        import settings # Assumed to be in the same directory.
    except ImportError:
        import sys
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)

from django.core.management import setup_environ
setup_environ(settings)
from skel.core.management import execute_manager
if __name__ == "__main__":
    execute_manager(settings)