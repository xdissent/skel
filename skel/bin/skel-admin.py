#!/usr/bin/env python

import sys
import optparse
import re
import subprocess
from random import choice
from paver.defaults import *

PROJECT_FILES = [
    '__init__.py',
    'local_settings.py',
    'manage.py',
    'requirements.txt',
    'settings_dev.py',
    'settings.py',
    'static',
    'templates',
    'urls.py',
]


def startproject(project_name=None, project_path=None, skel_path=None, venv=None):
    pass


def main(args=None):
    # get at the arguments
    if args is None:
        if len(sys.argv) > 1:
            args = sys.argv[1:]
        else:
            args = []
    
    # parse options
    usage = "Usage: %prog [global options] command [command options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-E', '--environment', metavar='VENV',
                      help='create or use a virtualenv at VENV')
    parser.disable_interspersed_args()
    options, args = parser.parse_args()
    
    if len(args) < 2:
        parser.error('incorrect number of arguments')
        
    if args[0] != 'startproject':
        parser.error('command must be "startproject"')
        
    project_path = path(args[1])
    
    if project_path.exists():
        parser.error('%s conflicts with the name of an existing file. Please use a different name or specify an absolute path.' % project_path)

    project_name = project_path.name
    
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        parser.error('%s conflicts with the name of an existing Python module and cannot be used as a project name. Please try another name.' % project_name)
    
    try:
        import skel
        skel_path = path(skel.__path__)
    except ImportError:
        skel_path = path(__file__).abspath().parent.parent


    if options.environment:
        venv_path = path(options.environment)
        if venv_path.isdir():
            activate_this = venv_path.joinpath('bin/activate_this.py')
            if not activate_this.exists():
                parser.error('VENV must point to a virtualenv if it exists.')
            execfile(activate_this, dict(__file__=activate_this))
        elif venv_path.exists():
            parser.error('VENV must point to a virtualenv if it exists.')
        else:
            # TODO: virtualenv creation script
            parser.error('here is where we would create a virtualenv for you.')
            
    project_path.mkdir(mode=0755)
    
    for file_path in PROJECT_FILES:
        src_path = skel_path.joinpath(file_path)
        dest_path = project_path.joinpath(file_path)
        if src_path.isdir():
            src_path.copytree(dest_path)
        else:
            src_path.copy(dest_path)
        
    local_settings_file = project_path.joinpath('local_settings.py')
    local_settings_contents = local_settings_file.text()
    local_settings_contents = re.sub(r"(?<=VIRTUAL_ENVIRONMENT_PATH = ').*'", venv_path.abspath() + "'", local_settings_contents)
    local_settings_file.write_text(local_settings_contents)
    
    settings_file = project_path.joinpath('settings.py')
    settings_contents = settings_file.text()
    secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    settings_contents = re.sub(r"(?<=SECRET_KEY = ').*'", secret_key + "'", settings_contents)
    settings_file.write_text(settings_contents)
    
    # TODO: install reqs even if no venv set? maybe don't need to cause skel and deps are already installed?
    if venv_path:
        # easy_install pip
        easy_install_path = venv_path.joinpath('bin/easy_install')
        if easy_install_path.exists():
            subprocess.call([easy_install_path, 'pip'])
        # copy skel to venv
        new_skel_path = venv_path.joinpath('lib/python%s/site-packages/skel' % sys.version[:3])
        skel_path.copytree(new_skel_path)
        pip_path = venv_path.joinpath('bin/pip')
        req_path = project_path.joinpath('requirements.txt')
        subprocess.call([pip_path, 'install', '-r', req_path])

if __name__ == '__main__':
    sys.exit(main())