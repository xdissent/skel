# Custom comment functions for settings.COMMENTS_APP = 'skel.comments'
def get_model():
    from skel.comments.models import Comment
    return Comment
    
def get_form():
    from skel.comments.forms import CommentForm
    return CommentForm