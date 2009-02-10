#!/usr/bin/env python

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

try:
    import os
    activate_this = os.path.join(settings.VIRTUAL_ENVIRONMENT_PATH, 'bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))
except:
    # TODO: catch 'missing file' exception
    # TODO: catch 'missing VIRTUAL_ENVIRONMENT_PATH setting'
    import sys
    print "Unexpected error:", sys.exc_info()[0]
    raise

from django.core.management import execute_manager

if __name__ == "__main__":
    execute_manager(settings)
#     setup_environ(settings)
#     project_path = path(settings.__file__).parent
#     pavement_file = path.joinpath(project_path, 'pavement.py')
#     if not pavement_file.exists():
#         import sys
#         sys.stderr.write("Error: Can't find the file 'pavement.py' in the directory containing %r.\n" % __file__)
#         sys.exit(1)
#     
#     from skel.core.management import ManagementUtility
#     utility = ManagementUtility()
#     utility.execute()
