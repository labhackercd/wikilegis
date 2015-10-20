# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.text import force_unicode


def parse_extra_classes(extra_classes):
    if isinstance(extra_classes, basestring):
        extra_classes = force_unicode(extra_classes)
        extra_classes = extra_classes.split(' ')
    return extra_classes
