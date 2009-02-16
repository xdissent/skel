Skel Remote Deployment
======================


Base Setup Deploy
-----------------

* ``mkvirtualenv project_name``

* ``svn co file:///home/36218/data/svn/project_name/trunk /home/36218/containers/django/project_name``

* ``easy_install pip``

* ``pip install -r /home/36218/containers/django/project_name/requirements.txt``

* ``python /home/36218/containers/django/project_name/setup.py develop``

* Fix ``VIRTUAL_ENVIRONMENT_PATH`` in ``local_settings.py``.

* ``/home/36218/containers/django/project_name/manage.py syncdb``


Skel Setup Deploy
-----------------

* Fix egg-links for development packages:

  - django
  - django-tagging
  - django-template-utils
  - django-profiles
      
  .. sourcecode:: bash

     BAD_PATH=nfs/c01/h07/mnt;
     for EGG_LINK in $VIRTUAL_ENV/lib/python*/site-packages/*.egg-link;
     do
         head -n 1 $EGG_LINK | sed "s:$BAD_PATH:home:" >> /home/36218/containers/django/mt_virtualenvs/project_name/lib/python2.4/site-packages/virtualenv_path_extensions.pth;
     done
  
* ``mtd add project_name /home/36218/containers/django/project_name projectname.com``

* ``mtd generate_htaccess project_name``

* Generate default ``mt_lighttpd.conf`` file.

  ``mtd start project_name && mtd stop project_name``
  
* Add ``/static/`` URL rewrite to ``/home/36218/containers/django/project_name/static/`` in ``/home/36218/containers/django/mt_runtime/mt_lighttpd.conf``.


Skel Clean Deploy
-----------------

* ``mtd remove project_name``

* ``rmvirtualenv project_name``

* ``rm -rf /home/36218/containers/django/project_name``

* Call **Base Setup Deploy**.
