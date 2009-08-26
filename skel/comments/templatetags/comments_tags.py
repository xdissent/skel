from django import template
from django.template.loader import render_to_string
from django.contrib.comments.templatetags.comments import CommentListNode, BaseCommentNode


register = template.Library()


class RenderCommentListNode(CommentListNode):
    """Render the comment list directly.
    
    From http://code.djangoproject.com/ticket/10285
    
    """
    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_list and return a Node."""
        tokens = token.contents.split()
        if tokens[1] != 'for':
            msg = 'Second argument in %r tag must be "for".' % tokens[0]
            raise template.TemplateSyntaxError(msg)

        if len(tokens) == 3:
            # {% render_comment_list for obj %}
            return cls(object_expr=parser.compile_filter(tokens[2]))
        elif len(tokens) == 4:
            # {% render_comment_list for app.models pk %}
            ctype = BaseCommentNode.lookup_content_type(tokens[2], tokens[0])
            object_pk_expr = parser.compile_filter(tokens[3])
            return cls(ctype=ctype, object_pk_expr=object_pk_expr)

    def render(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return ''
        template_search_list = [
            'comments/%s/%s/list.html' % (ctype.app_label, ctype.model),
            'comments/%s/list.html' % ctype.app_label,
            'comments/list.html'
        ]
        qs = self.get_query_set(context)
        comment_list = self.get_context_value_from_queryset(context, qs)
        dct = {'comment_list': comment_list}
        context.push()
        liststr = render_to_string(template_search_list, dct, context)
        context.pop()
        return liststr


@register.tag 
def render_comment_list(parser, token): 
    """Render the comment list for an object.

    Syntax::
        {% render_comment_list for [object] %}
        {% render_comment_list for [app].[model] [object_id] %}

    """
    return RenderCommentListNode.handle_token(parser, token) 