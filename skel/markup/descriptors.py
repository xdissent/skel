from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from skel.markup.models import MarkedUpItem


class MarkedUpDescriptor(object):
    """A descriptor that provides easy access to a ``MarkedUpItem`` object
    corresponding to each instance of the model containing the descriptor
    instance.
    
    """
    def __init__(self, source_field):
        """Initializes the descriptor instance.
        
        The ``source_field`` argument should be the name of the field on 
        which this descriptor is based.
        
        """
        self.source_field = source_field
        
    def __get__(self, instance, owner):
        """Returns a ``MarkedUpItem`` instance for an object.
        
        A ``MarkedUpItem`` object will be instantiated with the appropriate
        ``source_field``, ``content_type`` and (optionally) ``object_id``
        values for the instance from which the descriptor was accessed. This
        object will be cached into the instance and returned. If the instance
        object already has a cached ``MarkedUpItem`` instance, that will be 
        returned instead, and no new ``MarkedUpItem`` instance will be created,
        but not saved.
        
        """
        if instance is None:
            raise AttributeError('Must be accessed by instance.')
        cache_attr = ''.join(['_', self.source_field, '_markedup_item'])
        markedup_item = getattr(instance, cache_attr, None)
        if markedup_item is not None:
            return markedup_item
        content_type = ContentType.objects.get_for_model(owner)
        init_kwargs = {'content_type': content_type, 
                       'source_field': self.source_field}
        if instance.pk is not None:
            init_kwargs['object_id'] = instance.pk
            try:
                markedup_item = MarkedUpItem.objects.get(**init_kwargs)
            except ObjectDoesNotExist:
                pass
        if markedup_item is None:
            markedup_item = MarkedUpItem(**init_kwargs)
        setattr(instance, cache_attr, markedup_item)
        return markedup_item

    def __set__(self, instance, value):
        raise AttributeError('Read-only attribute.')

    def __delete__(self, instance):
        raise NotImplementedError