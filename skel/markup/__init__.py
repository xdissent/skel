# Global dict of models that have been registered with the Markup Editor.
registered_models = {}

def register(model, fields=None):
    """Registers a model's fields to be used with the Markup Editor.
    
    If fields is not specified, ``SKEL_MARKUP_MODEL_FIELDS`` will be checked 
    for a key corresponding to the model's name in the form ``app.model``. 
    If found, the value for that key should be a list of which models to 
    register. If no model specific value exists, all ``TextField`` fields 
    will be registered.
    
    """
    global registered_models
    from django.db.models.fields import TextField
    from skel.markup import settings
    from skel.markup.descriptors import MarkedUpDescriptor

    model_name = '.'.join([model._meta.app_label, model._meta.module_name])
    if model_name not in registered_models:
        # Initialize field registry for this model.
        registered_models[model_name] = []
    # Create fields list if it's not provided in the arguments.
    if fields is None:
        if model_name in settings.SKEL_MARKUP_MODEL_FIELDS:
            # Get field list from settings.
            fields = settings.SKEL_MARKUP_MODEL_FIELDS[model_name]
        else:
            # Add all TextField fields to our field list.
            fields = [field.name for field in model._meta.fields 
                      if field.__class__ is TextField]
    registered_models[model_name] = list(set(fields + registered_models[model_name]))
    # Add marked up descriptor to registered model fields.
    for field in fields:
        markedup_attr = ''.join([field, '_markedup'])
        setattr(model, markedup_attr, MarkedUpDescriptor(field))