import sys
from paver.tasks import *

class SkelTask(Task):
    pass

def skel_task(func):
    """Specifies that this function is a Skel task.
    
    Note that this decorator does not actually replace the function object.
    It just keeps track of the task and sets an is_task flag on the
    function object."""
    if isinstance(func, SkelTask):
        return func
    task = SkelTask(func)
    return task

class ProjectTask(Task):
    pass
    
def project_task(func):
    """Specifies that this function is a project task.
    
    Note that this decorator does not actually replace the function object.
    It just keeps track of the task and sets an is_task flag on the
    function object."""
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
        
def install_project_tasks():
    """Makes project Paver commands available as Paver tasks."""
    if not hasattr(environment, "_project_tasks_installed"):
        environment.task_finders.append(ProjectTaskFinder())
        environment._project_tasks_installed = True

@skel_task
def startproject():
    """Start a new Skel project."""
    print 'start project'
    
@cmdopts([
    ('username=', 'u', 'Username to use when logging in to the servers')
])
@project_task
def deploy(options):
    """Deploy a Skel project."""
    print 'Deployed %s' % options
    
@skel_task
def startapp():
    """Deploy a Skel project."""
    print 'deployed'

@skel_task
def demo(options):
    print 'demoing!'
    # get temp path
    # startproject()
    # call syncdb
    # call migrate
    # call runserver [--settings=settings_dev]
    # remove temp path