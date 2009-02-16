from django import template
from django.conf import settings
from template_utils.nodes import GenericContentNode

class LatestTweetsNode(GenericContentNode):
    def _get_query_set(self):
        users = getattr(settings, 'TWITTER_USERS', [])
        if not users:
            return users
        return [list(self.query_set.filter(user__screen_name__exact=user).order_by('-pub_time')[:self.num]) for (user, p) in users]
        
    def get_content(self, context):
        result = self._get_query_set()
        return { self.varname: result }
        
def do_latest_tweets(parser, token):
    """
    Example::
    
        {% get_latest_tweets 1 as latest_tweets %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes 3 arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return LatestTweetsNode('twitter.tweet', bits[1], bits[3])

register = template.Library()
register.tag('get_latest_tweets', do_latest_tweets)