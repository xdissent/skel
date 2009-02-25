class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass

registry = []

def register(model, categories_descriptor_attr='categories'):
    """
    Sets the given model class up for working with categories.
    """
    if model in registry:
        raise AlreadyRegistered(
            'The model %s has already been registered.') % model.__name__
    registry.append(model)
    
    from django.db import models
    from skel.categories.models import Category

    categories_field = models.ManyToManyField(Category, blank=True, null=True)
    categories_field.creation_counter = model._meta.fields[-1].creation_counter
    model.add_to_class(categories_descriptor_attr, categories_field)