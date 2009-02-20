from django import template
from template_utils.nodes import GenericContentNode

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


def do_all_objects(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return AllGenericContentNode(bits[1], 0, bits[3])
    
    
register = template.Library()
register.tag('get_all_objects', do_all_objects)