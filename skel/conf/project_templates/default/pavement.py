from paver.easy import *

# Hack for skel demo
import sys
sys.path.append('/Users/xdissent/Sites/hartzog_skel')

from skel.core.management.tasks import install_skel_tasks, install_project_tasks
install_skel_tasks()
install_project_tasks()
