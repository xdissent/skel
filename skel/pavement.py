README = path('README.txt').text()

options(
    setup=Bunch(
        name='skel',
        packages=['skel'],
        package_dir={'': '..'},
        version='0.1',
        author='Greg Thornton',
        author_email='xdissent@gmail.com',
        long_description = README,
        url='http://hartzogcreative.com'
    )
)

@task
@needs(['generate_setup', 'minilib', 'setuptools.command.sdist'])
def sdist():
    pass