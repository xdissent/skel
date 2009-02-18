# from django.core.management import ManagementUtility as DjangoManagementUtility
# from paver.defaults import *
# from paver.command import load_build, finalize_env
# 
# 
# class ManagementUtility(DjangoManagementUtility):
#     def __init__(self, source):
#         load_build(source)
#         finalize_env(options)
#         super(ManagementUtility, self).__init__()
#         
#     def main_help_text(self):        
#         usage = super(ManagementUtility, self).main_help_text()
#         usage += '\n\nSkel subcommands\n'
#         for name, task in TASKS.items():
#             if task.user_defined:
#                 usage = usage + '  %s\n' % name
#         return usage
#     
#     def execute(self):
#         print 'argv: %s' % self.argv
#         #call_task(self.argv[1])            
#         super(ManagementUtility, self).execute()

#from pkg_resources import resource_filename

#def launch_paver():
#    pavement_path = resource_filename('', 'pavement.py')
#    print 'launching pavement.py at %s' % pavement_path