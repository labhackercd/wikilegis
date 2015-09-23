# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.sites.shortcuts import get_current_site
import django_comments


def create_comment(request, content_object, author, comment):
    site = get_current_site(request)
    comment_model = django_comments.get_model()
    new_comment = comment_model(content_object=content_object, user=author, comment=comment, site=site)
    new_comment.save()
    return new_comment
