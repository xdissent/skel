
# Global dict of models that have been registered with the Markup Editor.
registered_models = {}

def register_model(model, fields=None):
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
    if model_name in registered_models:
        return
    if fields is None:
        if model_name in settings.SKEL_MARKUP_MODEL_FIELDS:
            fields = settings.SKEL_MARKUP_MODEL_FIELDS[model_name]
        else:
            fields = [field.name for field in model._meta.fields 
                      if field.__class__ is TextField]
    registered_models[model_name] = fields
    for field in fields:
        markedup_attr = '%s_markedup' % field
        setattr(model, markedup_attr, MarkedUpDescriptor(field))