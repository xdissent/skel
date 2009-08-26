# Custom comment functions for settings.COMMENTS_APP = 'skel.comments'    
def get_form():
    from skel.comments.forms import CommentForm
    return CommentForm