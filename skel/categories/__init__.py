
registered_models = []

def register(model, attr='categories'):
    """Sets the given model class up for working with categories."""
    model_name = '.'.join([model._meta.app_label, model._meta.module_name])
    if model_name not in registered_models:
        registered_models.append(model_name)
    
    # Delay imports to prevent weirdness.
    from django.db import models
    from skel.categories.models import Category

    # Add categories descriptor, which is just a field for now.
    field = models.ManyToManyField(Category, blank=True, null=True)
    field.creation_counter = model._meta.fields[-1].creation_counter
    model.add_to_class(attr, field)