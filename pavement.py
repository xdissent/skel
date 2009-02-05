import os

README = path('README.txt').text()
VERSION = '0.1'

PACKAGE_DATA = setuputils.find_package_data()

PACKAGES = [
    'skel',
    'skel.accounts',
    'skel.blog',
    'skel.core',
    'skel.portfolio',
]

SCRIPTS = [
    'skel/bin/skel-admin.py',
]


options(
    setup=Bunch(
        name='hartzog-skel',
        version=VERSION,
        description='The Hartzog Creative Skel Framework for Django',
        long_description = README,
        author='Greg Thornton',
        author_email='xdissent@gmail.com',
        url='http://hartzogcreative.com/projects/skel/',
        download_url='http://hartzogcreative.com/projects/skel/download/v%s/' % VERSION,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities',
        ],
    )
)


@task
@needs(['clean', 'generate_setup', 'minilib', 'setuptools.command.sdist'])
def sdist():
    pass
    
    
@task
@needs(['distutils.command.clean'])
def clean():
    remove = [
        'paver-minilib.zip',
        'setup.py',
        'dist',
        'hartzog_skel.egg-info',
    ]
    for fp in remove:
        fp = path(fp)
        if fp.exists():
            try:
                fp.remove()
            except OSError:
                fp.rmtree()