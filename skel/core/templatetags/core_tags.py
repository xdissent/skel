from django import template
from django.db.models import get_model
from template_utils.nodes import ContextUpdatingNode, GenericContentNode

class AllGenericContentNode(GenericContentNode):
    def get_content(self, context):
        query_set = self._get_query_set()
        if self.num == 1:
            result = query_set[0]
        elif self.num == 0:
            result = list(query_set)
        else:
            result = list(query_set[:self.num])
        return { self.varname: result }
        

class RetrieveObjectBySlugNode(ContextUpdatingNode):
    """
    ``Node`` subclass which retrieves a single object -- by
    slug lookup -- from a given model.

    Because this is a slug lookup, it is assumed that no other
    filtering is needed; hence, the settings-based filtering performed
    by ``GenericContentNode`` is not used here.
    
    """    
    def __init__(self, model, slug, varname):
        self.slug = template.Variable(slug)
        self.varname = varname
        self.model = get_model(*model.split('.'))
        if self.model is None:
            raise template.TemplateSyntaxError("Generic content tag got invalid model: %s" % model)
    
    def get_content(self, context):
        return { self.varname: self.model._default_manager.get(slug=self.slug.resolve(context))}


def do_all_objects(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return AllGenericContentNode(bits[1], 0, bits[3])
    

def do_retrieve_object_by_slug(parser, token):
    """
    Retrieves a specific object from a given model by slug
    lookup, and stores it in a context variable.
    
    Syntax::
    
        {% retrieve_object_slug [app_name].[model_name] [slug] as [varname] %}
    
    Example::
    
        {% retrieve_object_slug core.category "featured" as my_flat_page %}
    
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return RetrieveObjectBySlugNode(bits[1], bits[2], bits[4])
    
    
register = template.Library()
register.tag('get_all_objects', do_all_objects)
register.tag('retrieve_object_slug', do_retrieve_object_by_slug)