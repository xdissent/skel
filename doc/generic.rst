Skel Generic Application
========================


Installation
------------

The generic application requires no changes to your project settings. This
will change when the app provides template tags.


Views
-----

Class based versions of django.views.generic equivalents.

Wishlist:

 * Method to generate a URLConf for a view instance.
 * **DONE** No need to subclass view to make it model specific.
 * **DONE** Template search lists include object specific names.
 * ``LatestView`` view that takes multiple querysets and renders a list of
   objects applying the ``render_listing`` template tag to each object
   regardless of type.
 * A ``render_listing`` template tag that renders the object into a template
   that is determined based on an optional tag parameter or the object's app 
   name, model name, and object id, with a generic template provided as a 
   default. When called like ``{% render_listing entry "my_listing.html" %}``
   the template search list might look something like this:
   
   .. sourcecode:: python
   
       ['my_listing.html',
        'blog/entry_42_listing.html',          # entry.pk == 42
        'blog/entry_lorem-ipsum_listing.html', # entry.slug == 'lorem-ipsum'
        'blog/entry_listing.html',
        'blog/listing.html',
        'generic/listing.html']

 * **DONE** ``DetailView`` should default to a ``generic/detail.html`` template which
   handles a few reasonable default model attributes.
 * Date based views should be paginated.


``GenericView``
~~~~~~~~~~~~~~~

The base class for all generic views is ``GenericView``. It includes a 
mechanism for setting and retrieving configuration values by searching the
class and instance attributes, allowing the user to override these values
in a number of ways. For example, the following are equivalent:

    .. sourcecode:: python
    
        class MyView(GenericView):
            template_name = 'generic.html'

        view = GenericView(template_name='generic.html')


``ListView``
~~~~~~~~~~~~

Renders a list of objects into the appropriate template.

Notes:

 * Pagination included if you specify ``paginate_by`` option.
 * Even when providing ``template_obj_name`` option, the context will have
   an ``object_list`` variable containing the list items.
 * If you don't specify a queryset via the ``items`` or ``queryset`` options,
   the default template used will default to ``generic/list.html``. Otherwise,
   the template search list will include defaults based on the queryset's 
   app and model names. For example:
   
    .. sourcecode:: python
    
        from skel.blog.models import Entry

        class EntryList(ListView):
            template_name = 'my_entry_list.html'
            queryset = Entry.objects.all()

   The ``EntryList`` view will search for the following templates in order:
   
    * ``my_entry_list.html``
    * ``blog/entry_list.html``
    * ``blog/list.html``
    * ``generic/list.html``
    

``DetailView``
~~~~~~~~~~~~~~

Renders a detailed representation of an object.

Notes:

 * The template search path is similar to that of ``ListView``, except it 
   accounts for the primary key of the object as well as the object's slug. 
   The ``slug_field`` parameter must be set if the ``SlugField`` is not named
   "slug" in the model. An example template search path:
   
    * ``my_entry_detail.html`` (if specified in the ``template_name`` option)
    * ``blog/entry_42_detail.html`` (if the object's id is 42)
    * ``blog/entry_lorem-ipsum_detail.html`` (if the objects's slug is "lorem_ipsum")
    * ``blog/entry_detail.html``
    * ``blog/detail.html``
    * ``generic/detail.html``

  
``DateView``
~~~~~~~~~~~~

A base class for date based generic views.

Notes:
 * This view is not paginated.