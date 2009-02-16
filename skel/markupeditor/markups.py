from django.contrib.markup.templatetags import markup as markup_tags

registry = {}

def get_choices():
    return [(k, v.label) for k, v in registry.iteritems()]

class Markup(object):
    label = 'Generic Markup'
    
    def render(self, content):
        return content


class MarkdownMarkup(Markup):
    label = 'Markdown'
    
    def render(self, content):
        return markup_tags.markdown(content)

        
class RestructuredTextMarkup(Markup):
    label = 'restructuredText'
    
    def __init__(self):
        try:
            import restdirective
        except ImportError:
            pass

    def render(self, content):
        return markup_tags.restructuredtext(content)


class XHTMLMarkup(Markup):
    label = 'XHTML'
    
            
def register(markup, name):
    if name not in registry:
        registry[name] = markup

register(MarkdownMarkup, 'markdown')
register(RestructuredTextMarkup, 'rest')
register(XHTMLMarkup, 'xhtml')