from paver.easy import *
from paver.tasks import consume_args
import paver.doctools
import paver.setuputils
import paver.misctasks

paver.setuputils.install_distutils_tasks()

import os
from setuptools import find_packages

PROJECT_FILES = [
    '__init__.py',
    'local_settings.py',
    'manage.py',
    'settings_dev.py',
    'settings.py',
    'static',
    'templates',
    'urls.py',
]

PROJECTS_DIR = os.environ.get('SKEL_PROJECTS_DIR', '~/Sites/')
SVN_URL_ROOT = os.environ.get('SKEL_SVN_URL_ROOT', 'svn+ssh://hartzogcreative.com@hartzogcreative.com/home/36218/data/svn/')
SVN_SSH_HOST = os.environ.get('SKEL_SVN_SSH_HOST', 'hzc.com')
SVN_SSH_ROOT = os.environ.get('SKEL_SSH_ROOT', '/home/36218/data/svn/')
ENVIRONMENTS_DIR = os.environ.get('SKEL_ENVIRONMENTS_DIR', False)
if not ENVIRONMENTS_DIR:
    ENVIRONMENTS_DIR = os.environ.get('WORKON_HOME', False)
    
PACKAGE_DATA = paver.setuputils.find_package_data()
#print PACKAGE_DATA
PACKAGES = sorted(PACKAGE_DATA.keys())
PACKAGES = find_packages()
print PACKAGES

DATA_FILES = [
    ('skel/core/management', ['pavement.py']),
]

options(
    setup=Bunch(
        name='Skel',
        version='0.1',
        description='Hartzog Creative Skel Framework for Django',
        author='Greg Thornton',
        author_email='xdissent@gmail.com',
        packages=PACKAGES,
        package_data={
            'skel.core.management': ['pavement.py'],
        },
        zip_safe=False,
        entry_points = {
            'console_scripts': [
                'skel-admin.py = skel.core.management:launch_paver',
            ],
        },
        include_package_data=True,
        data_files=DATA_FILES,
    ),
    minilib=Bunch( 
        extra_files=['doctools', 'setuputils']
    ), 
    startproject=Bunch(
        projects_dir=PROJECTS_DIR,
        svn_url_root=SVN_URL_ROOT,
        environments_dir=ENVIRONMENTS_DIR,
        environment=False,
        svn_ssh_host=SVN_SSH_HOST,
        svn_ssh_root=SVN_SSH_ROOT,
        svn_dev_branch='xdissent'
    )
)


@task
def copyfiles():
    pass


@task
@cmdopts([
    ('no-coda', None, 'Disable Site creation in Coda'),
    ('no-svn', None, 'Disable Subversion repository creation'),
    ('environment=', 'E', 'Use a virtualenv for the environment'),
    ('no-upgrade', None, 'Prevent updating Skel in the virtualenv'),
    ('no-requirements', None, 'Prevent Virtualenv from being populated with requirements')
])
@consume_args
def startproject(options):
    """Starts a new Skel project"""
    info('pavement %s' % environment.pavement_file)
    
    project_path = path(options.args[0])
    project_name = project_path.name
    
    if project_name == project_path:
        projects_dir = path(options.projects_dir).expand()
        project_path = path.joinpath(projects_dir, project_name)
        
    if project_path.exists():
        raise BuildFailure('Project already exists at %s' % project_path)
        
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        raise BuildFailure('Python module named %s already exists on your path' % project_path)
    
    svn_url_root = path(options.svn_url_root)
    svn_url = path.joinpath(svn_url_root, project_name)
    
    if 'no-svn' not in options.startproject:
        try:
            info('Checking for project name collision at %s' % svn_url)
            sh('svn ls %s' % svn_url)
        except BuildFailure:
            pass
        else:
            raise BuildFailure('Project already in subversion at %s' % svn_url)
    
    dry('Creating project directory at %s' % project_path, project_path.mkdir)
    
    environments_dir = path(options.environments_dir)
    venv_path = environments_dir.joinpath(project_name)
    if options.environment:
        venv_path = path(options.environment)
    venv_path = venv_path.expand()
        
    if venv_path.exists():
        if not venv_path.joinpath('bin/activate').exists():
            raise BuildFailure('Folder at %s does not contain a Virtualenv' % venv_path)
        info('Using existing virtualenv at %s' % venv_path)
    else:
        info('Creating virtualenv for %s at %s' % (venv_path, project_name))
        sh('virtualenv %s' % venv_path)
    
    easy_install_path = venv_path.joinpath('bin/easy_install')
    if not easy_install_path.exists():
        raise BuildFailure('Virtualenv at %s does not contain easy_install' % venv_path)
    
    try:
        import skel
    except ImportError:
        print "*** STILL CANT IMPORT"
    else:
        print "*** IMPORTED"
        
    # TODO: figure out skel_path
    skel_path = path('~/Sites/hartzog-skel/skel/').expand()
    
    if 'no-requirements' not in options.startproject:
    
        info('Easy installing PIP to process requirements.txt')
        sh('%s pip' % easy_install_path)
        
        pip_path = venv_path.joinpath('bin/pip')
        
        # TODO: handle skel upgrade option and set skel_path appropriately
        # if no upgrade, run paver install task into virtualenv
        # if upgrade run pip install skel
        # import skel
            
        # TODO: get skel pkg_resources path as skel_path
        # TODO: get requirements_path from skel pkg_resources:
        # requirements_path = skel_path.joinpath('requirements.txt')
        requirements_path = path('~/Sites/hartzog-skel/requirements.txt').expand()
        
        info('Installing requirements with PIP')
        sh('%s install -r %s' % (pip_path, requirements_path))
        
        
    if 'no-svn' not in options.startproject:
        svn_ssh_root = path(options.svn_ssh_root)
        svn_ssh_path = svn_ssh_root.joinpath(project_name)
        
        svnadmin_command = 'svnadmin create %s' % svn_ssh_path
        ssh_command = "ssh %s '%s'" % (options.svn_ssh_host, svnadmin_command)
        info('Creating repository using "%s"' % ssh_command)
        sh(ssh_command)
        sh('svn mkdir %s -m "creating %s"' % (svn_url.joinpath('trunk'), 'trunk'))
        sh('svn mkdir %s -m "creating %s"' % (svn_url.joinpath('tags'), 'tags'))
        sh('svn mkdir %s -m "creating %s"' % (svn_url.joinpath('branches'), 'branches'))
        
        svn_dev_branch_url = svn_url.joinpath('branches', options.svn_dev_branch)
        sh('svn mkdir %s -m "creating development branch (%s)"' % (svn_dev_branch_url, svn_dev_branch_url))
        
        sh('svn co %s %s' % (svn_dev_branch_url, project_path))
        # TODO: set svnignores
    
    # TODO: fix into pkg_resources instead of skel_path
    info('Copying default files from %s to %s' % (skel_path, project_path))
    for file_path in PROJECT_FILES:
        src_path = skel_path.joinpath(file_path)
        dest_path = project_path.joinpath(file_path)
        
        if src_path.isdir():
            src_path.copytree(dest_path)
        else:
            src_path.copy(dest_path)
            
    from pprint import pprint
    pprint(options.startproject)