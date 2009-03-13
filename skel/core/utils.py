from django import template

def render_into_response(response, *args, **kwargs):
    target = kwargs.pop('target', 'body')
    position = kwargs.pop('position', 'first')
    to_insert = template.loader.render_to_string(*args, **kwargs)
    if position == 'first':
        response.content = response.content.replace(u'<%s>' % target, 
                u'<%s>%s' % (target, to_insert))
    else:
        response.content = response.content.replace(u'</%s>' % target, 
                u'%s</%s>' % (to_insert, target))
    return response