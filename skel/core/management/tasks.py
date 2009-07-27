import os
import sys
from paver.path import path
from paver.tasks import *
from paver.easy import sh
from paver.options import Bunch

class SkelTask(Task):
    pass

class ProjectTask(Task):
    pass


def skel_task(func):
    """Specifies that this function is a Skel task.
    
    Note that this decorator does not actually replace the function object.
    It just keeps track of the task and sets an is_task flag on the
    function object.
    
    """
    if isinstance(func, SkelTask):
        return func
    task = SkelTask(func)
    return task


def project_task(func):
    """Specifies that this function is a project task.
    
    Note that this decorator does not actually replace the function object.
    It just keeps track of the task and sets an is_task flag on the
    function object.
    
    """
    if isinstance(func, ProjectTask):
        return func
    task = ProjectTask(func)
    return task


class SkelTaskFinder(object):
    def get_task(self, taskname):
        tasks = self.get_tasks()
        for task in tasks:
            if task.shortname == taskname:
                return task

    def get_tasks(self):
        skel_tasks = []
        module = sys.modules['skel.core.management.tasks']
        for name in dir(module):
            item = getattr(module, name, None)
            if isinstance(item, SkelTask):
                skel_tasks.append(item)
        return skel_tasks
        
class ProjectTaskFinder(SkelTaskFinder):
    def get_tasks(self):
        project_tasks = []
        module = sys.modules['skel.core.management.tasks']
        for name in dir(module):
            item = getattr(module, name, None)
            if isinstance(item, ProjectTask):
                project_tasks.append(item)
        return project_tasks


def install_skel_tasks():
    """Makes Skel Paver commands available as Paver tasks."""
    if not hasattr(environment, "_skel_tasks_installed"):
        environment.task_finders.append(SkelTaskFinder())
        environment._skel_tasks_installed = True
        environment.options(
            startproject=Bunch(
                no_svn=False,
                prefix=os.environ.get('SKEL_PREFIX', '~/Sites'),
                template=os.environ.get('SKEL_TEMPLATE', 'default'),
                svn_root=os.environ.get('SKEL_SVN_ROOT', 'https://code.hartzogcreative.com/svn'),
                virtualenv=None
            )
        )
        
def install_project_tasks():
    """Makes project Paver commands available as Paver tasks."""
    if not hasattr(environment, "_project_tasks_installed"):
        environment.task_finders.append(ProjectTaskFinder())
        environment._project_tasks_installed = True
        # Set up default options.


@cmdopts([
    ('prefix=', 'p', 'The base path to use for creating the project.'),
    ('no-svn', None, 'Disable Subversion repository creation.'),
    ('template=', 't', 'The Skel project template to use.'),
    ('svn-root=', None, 'The base path of your repository path. Eg: http://<yourserver>/svn'),
    ('virtualenv=', None, 'The virtualenv folder for this project. The virtualenv will be created if necessary.'),
])
@consume_args
@skel_task
def startproject(options, args, debug, info):
    """Start a new Skel project."""
    
    if not args:
        raise BuildFailure('This command requires one argument.')
    if 'startproject' not in options:
        raise BuildFailure('Could not find default options.')

    options = options.startproject
    debug('%s' % options)
#     raise BuildFailure('Stopping')
    
    skel_path = path(sys.modules['skel'].__file__).dirname()
    if not skel_path.exists():
        raise BuildFailure('Could not find Skel location.')
    info('Using Skel at %s' % skel_path)
    
    template_path = skel_path / 'conf/project_templates' / options.template
    if not template_path.exists():
        raise BuildFailure('Cound not find template "%s" in "%s".' % (options.template, template_path.dirname()))
    info('Using Skel template "%s" from "%s"' % (options.template, template_path))
    
    project_name = args[0]
    project_path = path(options.prefix) / project_name
    project_path = project_path.expanduser()
    
    if project_path.exists():
        raise BuildFailure('Project path "%s" already exists.' % project_path)

    info('Copying project template "%s" to "%s".' % (options.template, project_path))
    try:
        template_path.copytree(project_path)
    except OSError:
        raise BuildFailure('Could not create project directory "%s".' % project_path)
        
    if not options.no_svn:
        svn_url = path(options.svn_root) / project_name
        try:
            info('Checking for project name collision at %s.' % svn_url)
            sh('svn ls %s' % svn_url, capture=True)
        except BuildFailure:
            info('No SVN name collision found.')
            pass
        else:
            raise BuildFailure('Project already in subversion at %s.' % svn_url)

    if options.virtualenv is not None:
        mkvirtualenv_command = 'virtualenv %s' % options.virtualenv
        virtualenv_path = path(options.virtualenv)
    else:
        info('Detecting virtualenvwrapper.')
        virtualenvwrapper = None
        try:
            sh('source ~/.bash_profile && workon', capture=True)
        except BuildFailure:
            try:
                virtualenvwrapper = sh('which virtualenvwrapper_bashrc', capture=True).strip()
            except BuildFailure:
                info('Could not find virtualenvwrapper in path. (%s)' % virtualenvwrapper)
            else:
                info('Found virtualenvwrapper in PATH at "%s".' % virtualenvwrapper)
        else:
            virtualenvwrapper = '~/.bash_profile'
            info('Found virtualenvwrapper in .bash_profile.')
        
        if virtualenvwrapper is None:
            raise BuildFailure('Could not find virtualenvwrapper. You must specify the "--virtualenv=VENV_PATH" option.')

        mkvirtualenv_command = 'source %s && mkvirtualenv %s' % (virtualenvwrapper, project_name)
        virtualenv_path = path(sh('source %s && echo $WORKON_HOME' % virtualenvwrapper, capture=True).strip())
        
    try:
        sh(mkvirtualenv_command)
    except BuildFailure:
        raise BuildFailure('There was a problem creating the virtual environment.')

    easy_install_path = virtualenv_path / 'bin/easy_install'
    try:
        sh('%s pip' % easy_install_path, capture=True)
    except BuildError:
        raise BuildError('Could not install pip.')
    
    pip_path = virtualenv_path / 'bin/pip'
    info('Installing requirements into virtualenv.')
    try:
        sh('%s install -r %s' % (pip_path, project_path / 'requirements.txt'))
    except BuildFailure:
        raise BuildFailure('Error encountered while installing requirements.')
    
    info('Done creating project.')


@consume_args
@skel_task
def demo(info):
    """Run a temporary Skel demo server."""
    import tempfile
    temp_prefix = path(tempfile.mkdtemp())
    temp_project = temp_prefix / 'demo'
    temp_virtualenv = temp_prefix / 'virtualenv'
    temp_python = temp_virtualenv / 'bin/python'

    environment.options.startproject['no_svn'] = True
    environment.options.startproject['prefix'] = temp_prefix
    environment.options.startproject['virtualenv'] = temp_virtualenv
    environment.args = ['demo']
    
    info('Starting demo project.')
    try:
        startproject()
    except BuildFailure:
        info('Error encountered. Removing demo directory.')
        temp_prefix.rmtree()
        raise

    try:
        try:
            temp_manage_cmd = 'cd %s && %s ./manage.py' % (temp_project, temp_python)
            sh('%s syncdb --settings=settings_dev --migrate --noinput' % temp_manage_cmd)
            sh('%s runserver --settings=settings_dev' % temp_manage_cmd)
        except BuildFailure:
            info('Error encountered. Removing demo directory.')
            temp_prefix.rmtree()
            raise
    except KeyboardInterrupt:
        pass

    info('Demo stopped. Removing demo directory.')
    temp_prefix.rmtree()