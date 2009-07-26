The Life of a Skeletor:
=======================

Have an idea.
-------------

* *Define your idea.*

  Start with the general description which we'll use in 
  the requisite README.txt later.
  
* *Name your idea.*

  Any files needed by this idea will probably have to go
  into a folder along side those of other similar ideas. This means the 
  sooner we come up with a solid name for this particular idea, the less
  likely a name collision in filesystem storage as well as in other tools.
  If the idea deserves a domain name then nailing one down as quickly as
  possible can be very helpful down the road.

* *Brainstorm, then braindump.*

  Use productivity tools to document the
  concerns, questions, and plans rushing through your mind regarding this
  idea. Use the easy-to-read version of the idea's name.

Build your idea a home.
-----------------------

    .. sourcecode:: console
    
       $ skel-admin.py startproject [--no-svn] [--no-coda] \
       [-E <venv_path>|--environment=<venv_path>] [--no-upgrade] \
       <project_name|project_path>

* *Create a local folder.*

  A good file organization scheme can increase
  the likelihood of your ideas' success. Always keep similar ideas in a 
  logical structure on disk. Skel uses ``~/Sites/<project_name>`` as a 
  default location. This differs from the ``django-admin.py`` tool in that
  you must pass a relative path beginning with ``./`` or an absolute path.
  Otherwise the project will be created in ``~Sites/<project_name>``.
  Use ``$SKEL_PROJECTS_DIR`` to override this default path. Skel will exit
  with an error if a similarly named project or python module already exist.

* *Stay clean.*

  Using a single workstation to develop many ideas means working environments
  can experience cross-project contamination fairly easily. Skel requires
  Virtualenv and will optionally use Virtualenvwrapper to determine default
  paths for the project's environment and any hooks you've installed will
  run when the virtualenv is created. Skel creates a ``virtualenv`` calling
  ``[mk]virtualenv $SKEL_VENV_DIR/<project_name>`` or 
  ``[mk]virtualenv <project_name>`` if ``$SKEL_VENV_DIR`` is not found. If 
  ``-E <venv_path>`` or ``--environment=<venv_path>`` are provided, 
  ``[mk]virtualenv <venv_path>`` is used. If Skel cannot create an environment
  an error will occur.

* *Stay current.*

  Ideas tend to move pretty quickly when you have the right set of tools.
  Skel is constantly being updated to keep your workflow as efficient as
  possible, and things are often being added to the framework. Keeping up
  to date with the latest version of Skel is the recommended development
  practice for all projects. As a result, Skel will try to install the 
  newest release in your new project's environment. This means you won't
  have to migrate your project to the current version of Skel if you have
  forgotten to upgrade before running ``skel-admin.py``. You can provide
  ``--no-upgrade`` to force Skel to use the currently installed version.

* *Stop repeating yourself.*

  In most cases there are preexisting support 
  files that can serve as a springboard to launch your idea further down
  the development path. Skel copies default files into your new project,
  ready for customization. Installing the required Python modules takes 
  place automatically as well. In the future, Skel will also automatically 
  create a site entry for this project in Coda. This will be the default
  action unless suppressed with ``--no-coda``.

* *Never lose anything.*

  Keep your code safe by using Subversion. Pass the ``--no-svn`` option
  to prevent a repository from being created or supply ``$SKEL_SVN_HOST``, 
  ``$SKEL_SVN_USER``, ``$SKEL_SVN_PSWD`` and ``$SKEL_SVN_PATH`` to define
  how the repository should be created. If a project with the same
  name is already stored in the repository, an error will occur. Skel also
  adds ``trunk``, ``branches`` and ``tags`` directories to the repo, commits
  the default files to ``trunk``, and finally creates a development branch
  at ``branches/$LOGNAME``. The working copy at 
  ``$SKEL_PROJECTS_DIR/<project_name>`` or ``~/Sites/<project_name>`` will 
  contain this development branch.

Implement your idea.
--------------------

* *Enhance your tools.*

  TODO: Finalize these options and Coda Plugin specifications.
  
  If a task is too difficult to do easily *and* quickly, it probably
  will not get done, or at least will often be done incorrectly. Your 
  toolchain can be a hindrance to your development cycle unless the 
  individual utilities are well integrated with each other. Hartzog Creative
  uses Panic's Coda as it's unofficial *everything* editor. Skel includes
  a Coda Plugin that simplifies many common tasks in Coda. When activating
  a local Terminal from within a Skel Coda Site, the path is set to the 
  project's root folder and the virtualenv is activated automatically.
  Keyboard shortcuts are installed for ``skel-admin.py`` 
  commands. Use ``skel-admin.py codaplugin`` to install. If your Site 
  was created with ``startproject``, a startup command will be added that 
  calls Virtualenvwrapper's ``workon`` script for the project's virtual 
  environment as well as ``manage.py runserver``. Skel also includes 
  a set of Coda Clips with tons of useful shortcuts and time-saving 
  boilerplate code. Run ``skel-admin.py codaclips`` to install the 
  Coda Clips into Coda's library. Since Skel recommends using restructuredText 
  for most content, Skel includes commands to install language
  helpers for both editors. Use ``textmaterest`` or ``codarest`` to install
  either bundle.

* *Document everything.*

  The greatest ideas in the world are nothing if you can't use them. It's 
  even worse when you have to come back to a project in a few weeks and 
  you spend all day just trying to find your place. Skel makes heavy use
  of Sphinx-style documentation and less frequently, inline documentation.
  All projects are encouraged to follow this convention, and a ``doc`` folder
  is created for you automatically. The ``updatedocs`` command rebuilds your
  documentation from source. Paver can be used to produce very robust docs
  which will also automatically be served by your project's administrative
  interface, alongside the Django and Skel documentation. The ``doc/user/``
  folder will be served at ``/doc/`` by the project's media server.
  
* *Test first and often.*

  Use Django test conventions. ``manage.py test`` is provided already.
  Deployments will fail if all tests are not passed, so take this seriously.
  You *can* bypass testing upon deployment by passing the ``--no-test``
  option to ``manage.py deploy``. In our experience, code flow can often be 
  better understood and less likely to require refactoring if tests are 
  written first.
  
* *Collaborate with people smarter than you.*

  Working alongside other developers can be greatly beneficial to the 
  success of your project. The proposed Skel workflow provides methods
  to easily manage a Subversion repository for your code. Commands for
  branching, merging, repository creation, and even repository removal
  are available through ``skel-admin.py`` *and* ``manage.py`` so there's
  no reason to *not* practice consistent revision control.
  
  ``manage.py commit <msg>``
  @task('commit')
  @needs(['html', 'test'])
  svn ci -m <msg>
  
  commit and ``manage.py merge <msg>`` often.
  @task('merge')
  @needs(['commit'])
  svn merge trunk into working copy
  svn ci -m <msg>
  
  ``manage.py deploy``
  @task('deploy')
  @needs(['merge', 'commit'])
  commit development into trunk
  svn up trunk working copy at dev.domain.com
  runs remote tests
  mtd restarts project_name_dev
  make sure working copy is still development branch
  
  
  @task('release')
  @needs(['merge'])


* *Upgrade Tools* 

  Get Subversion from http://www.open.collab.net/downloads/community/
  Install it to opt. 
  
  Download http://www.open.collab.net/downloads/apple/download.html
  export PATH=/opt/subversion/bin:$PATH in .bash_profile
  add to .subversion/config: global-ignores = *.o *.lo *.la #*# .*.rej *.rej .*~ *~ .#* .DS_Store *.pyc
  pushd $HOME/.subversion && wget http://svn.collab.net/repos/svn/trunk/tools/client-side/bash_completion && popd
  export SVN_BASH_COMPL_EXT="urls svnstatus" in .bash_profile
  source "$HOME/.subversion/bash_completion in .bash_profile