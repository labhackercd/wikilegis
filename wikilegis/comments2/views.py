from django.contrib.auth.decorators import login_required
from django_comments.views.comments import post_comment

post_comment = login_required(post_comment)
