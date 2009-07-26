import os
import sys
import types
from django.core.management import ManagementUtility, setup_environ, get_commands

try:
    import paver
except ImportError:
    import skel
    skel_path = os.path.dirname(skel.__file__)
    paver_path = os.path.join(skel_path, 'paver-minilib.zip')
    print 'PAVER PATH: %s' % paver_path
    if os.path.exists(paver_path):
        sys.path.insert(0, paver_path)

from skel.core.management.tasks import *

def get_tasks(cls=None):
    if cls is None:
        task_list = [task.shortname for task in environment.get_tasks()]
    else:
        task_list = [task.shortname for task in environment.get_tasks() if task.__class__ is cls]
    return task_list
        
class Command(object):
    """A simple Django wrapper for calling Paver tasks."""
    def __init__(self, name):
        self.task = getattr(sys.modules['skel.core.management.tasks'], name)
            
    def print_help(self, prog_name, subcommand):
        self.run_from_argv()
        
    def run_from_argv(self, args=None):
        if args is None:
            args = sys.argv
        args = args[1:]
        args = parse_global_options(args)
        process_commands(args)

class SkelManagementUtility(ManagementUtility):
    """Encapsulates the logic of the skel-admin.py and manage.py utilities.

    A ManagementUtility has a number of commands, which can be manipulated
    by editing the self.commands dictionary.
    
    """

    def fetch_command(self, subcommand):
        """
        Tries to fetch the given subcommand, printing a message with the
        appropriate command called from the command line (usually
        "skel-admin.py" or "manage.py") if it can't be found.
        
        """
        
        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            if subcommand in get_tasks(ProjectTask):
                return Command(subcommand)
        if subcommand in get_tasks(SkelTask):
            return Command(subcommand)
        if subcommand in get_tasks(Task):
            return Command(subcommand)
        return super(SkelManagementUtility, self).fetch_command(subcommand)
        
    def main_help_text(self):
        """Returns the script's main help text, as a string."""
        usage = ['',"Type '%s help <subcommand>' for help on a specific subcommand." % self.prog_name,'']
        
        usage.append('Available Paver subcommands:')
        paver_commands = get_tasks(Task)
        for cmd in paver_commands:
            usage.append('  %s' % cmd)
        
        usage.append('\nAvailable Skel subcommands:')
        skel_commands = get_tasks(SkelTask)
        for cmd in skel_commands:
            usage.append('  %s' % cmd)

        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            usage.append('\nAvailable Project subcommands:')
            project_commands = get_tasks(ProjectTask)
            for cmd in project_commands:
                usage.append('  %s' % cmd)
            
        usage.append('\nAvailable Django subcommands:')
        commands = get_commands().keys()
        pavement_commands = get_tasks()
        commands = [cmd for cmd in commands if cmd not in pavement_commands]
        commands.sort()
        for cmd in commands:
            usage.append('  %s' % cmd)
        return '\n'.join(usage)
        
def execute_from_command_line(argv=None):
    execute_manager(argv=argv)
    
def execute_manager(settings_mod=None, argv=None):
    """
    Like execute_from_command_line(), but for use by manage.py, a
    project-specific skel-admin.py utility.
    
    """
    pavement_path = None
    if settings_mod is not None:
        setup_environ(settings_mod)
        pavement_path = os.path.join(os.path.dirname(settings_mod.__file__), 
                                                     'pavement.py')
    mod = types.ModuleType('pavement')
    environment.pavement = mod

    environment.pavement_file = pavement_path
    if pavement_path is None or not os.path.exists(pavement_path):
        exec """
from paver.easy import *
from skel.core.management.tasks import install_skel_tasks
install_skel_tasks()\n""" in mod.__dict__
    else:
        mod.__file__ = environment.pavement_file
        execfile(environment.pavement_file, mod.__dict__)
    utility = SkelManagementUtility(argv)
    utility.execute()