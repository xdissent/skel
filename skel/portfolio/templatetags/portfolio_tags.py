from django import template
from skel.portfolio.models import Section, Project

class SectionProjectsNode(template.Node):
    def __init__(self, section_slug, num, var_name):
        self.section_slug = template.Variable(section_slug)
        self.num = int(num)
        self.var_name = var_name
        
    def render(self, context):
        try:
            section = Section.objects.filter(slug__exact=self.section_slug.resolve(context))[0]
            if self.num == 0:
                context[self.var_name] = section.projects.all()
            else:
                context[self.var_name] = section.projects.all()[:self.num]
        except IndexError:
            pass
        return ''
            
        
def do_section_projects(parser, token):
    """
    Example::
    
        {% get_projects_for_section featured 3 as featured_projects %}
        {% get_projects_for_section featured as featured_projects %}
    
    """
    bits = token.contents.split()
    if len(bits) < 4:
        raise template.TemplateSyntaxError("'%s' tag takes at least 4 arguments" % bits[0])
    if bits [3] != 'as' and bits[2] != 'as':
        raise template.TemplateSyntaxError("second or third argument to '%s' tag must be 'as'" % bits[0])
    if bits[2] == 'as':
        return SectionProjectsNode(bits[1], 0, bits[3])
    return SectionProjectsNode(bits[1], bits[2], bits[4])
    
    
register = template.Library()
register.tag('get_projects_for_section', do_section_projects)