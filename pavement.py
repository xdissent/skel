import sys
from paver.easy import *
# import paver.doctools
from paver.setuputils import setup, find_package_data, find_packages

try:
    import skel
except ImportError:
    sys.path.insert(0, '')
    
from skel.core.management.tasks import install_skel_tasks
install_skel_tasks()

package_data = find_package_data('skel', package='skel', 
                                 only_in_packages=False)
packages = find_packages()
data_files = []

# print package_data
# print packages
# print data_files

setup(
    name='Skel',
    version='0.0.1',
    url='http://skel.hartzogcreative.com/',
    author='Greg Thornton',
    author_email='xdissent@gmail.com',
    description='The Hartzog Creative Django Framework',
    packages=packages,
    package_data=package_data,
    data_files=data_files,
    scripts=['bin/skel-admin.py'],
)