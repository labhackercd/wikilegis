from django.utils.text import slugify
import os


def references_filename(instance, filename):
    path = "bill/references/"
    fname = filename.split('.')
    file_format = slugify(fname[0]) + '.' + fname[-1]
    return os.path.join(path, file_format)


def theme_icon_filename(instance, filename):
    path = "bill/themes/"
    fname = filename.split('.')
    filename = slugify(fname[0]) + '.' + fname[-1]
    return os.path.join(path, filename)
