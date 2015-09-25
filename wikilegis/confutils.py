# -*- coding: utf-8 -*-
import string


SPLIT_CHAR = ','


def environ_to_int(value, default=0):
    if value is None:
        value = ''

    if isinstance(value, basestring):
        value = value.strip()

    try:
        return int(value)
    except:
        return default


def environ_to_boolean(value, default=False):
    """
    Turns value into a boolean. If it's `None` or empty, we'll return `default`.

    If it's a digit, we'll read it as an integer and then convert to boolean.

    If it's either `'false'`, `'no'` or `'off'` we return False.

    Otherwise it's True.
    """
    if not value:
        value = ''

    value = value.lower().strip()

    if value.isdigit():
        value = environ_to_int(value, default)
    elif value in ('false', 'no', 'off'):
        value = False

    return bool(value)


def environ_to_list_of_strings(value, split_char=SPLIT_CHAR):
    if not value:
        value = ''

    value = value.split(split_char)

    value = map(string.strip, value)

    return filter(bool, value)
