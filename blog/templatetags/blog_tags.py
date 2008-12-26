import md5
from django import template
from django.template.defaultfilters import stringfilter
from template_utils.nodes import GenericContentNode

class LatestCommentsNode(GenericContentNode):
    def _get_query_set(self):
        self.num = int(self.num)
        comments = list(self.query_set.order_by('-submit_date')[:self.num])
        cdict = {}
        for comment in comments:
            obj_label = '%s.%s-%s' % (comment.content_type.app_label, comment.content_type.model, comment.object_pk)
            if not obj_label in cdict:
                cdict[obj_label] = []
            cdict[obj_label].append(comment)
        comments = []
        for (k, comment_list) in cdict.items():
            comments += comment_list
        return comments
            
        
def do_latest_comments(parser, token):
    """
    Example::
    
        {% get_latest_comments 5 as latest_comments %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes 3 arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return LatestCommentsNode('comments.comment', bits[1], bits[3])
    
@stringfilter
def do_md5(value):
    return md5.new(value).hexdigest()

register = template.Library()
register.tag('get_latest_comments', do_latest_comments)
register.filter('md5', do_md5)
