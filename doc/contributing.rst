Contributing to Hartzog Skel
============================

Submit changes via patch
------------------------

* ``svn co svn+ssh://hartzogcreative.com@hartzogcreative.com/home/36218/svn/skel/trunk skel-trunk``

* ``python skel-trunk/setup.py develop``

* Make changes to skel-trunk/skel

* Ensure your changes merge cleanly:

  .. sourcecode:: console
  
     $ svn up
     M skel/
     ? skel/new_app
     [..]
     At revision 314.

* ``svn diff > ~/skel_new_app.diff``

* Create new issue on google code page or find relevant current issue and attach the patch.


Create a Subversion branch
--------------------------

* Request Subversion access.

* ``svn copy svn+ssh://hartzogcreative.com@hartzogcreative.com/home/36218/svn/skel/trunk
  svn+ssh://hartzogcreative.com@hartzogcreative.com/home/36218/svn/skel/branches/user
  -m "creating user branch"``

* ``svn co svn+ssh://hartzogcreative.com@hartzogcreative.com/home/36218/svn/skel/branches/user skel-user``

* ``python skel-user/setup.py develop

* Make changes to your branch.

* Commit often; always include a message:

  .. sourcecode:: console
  
     $ svn ci -m "adding that new feature" 

* Ensure your changes merge cleanly:

  .. sourcecode:: console
  
     $ svn merge svn+ssh://hartzogcreative.com@hartzogcreative.com/home/36218/svn/skel/trunk skel-user
     M skel/core/management/__init__.py
     A skel/superimage/templates/superimage/superimagewidget.html
     [..]
     At revision 358.
     
* Request merge back into trunk.