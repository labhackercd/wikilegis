from django import template
from django.apps import apps as django_apps
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

register = template.Library()

HELPERS_MODULE_NAME = 'helpers'

@register.simple_tag(takes_context=True)
def call(context, helper, *args, **kwargs):
    """
    The magical *call*. It takes a helper name (in the form of helper_name or app_label:helper_name)
    and it calls it with the given arguments (`*args` and `**kwargs`).

    Helpers are then resolved to functions of existing helper modules in installed applications.

    And then they are called with the given arguments.

    Like this:

        app/helpers.py:

            @nocontext
            def say_hello(user):
                return u"Hello, {0}!".format(user.get_full_name())

        sometemplate.html:

            {% load helpers %}
            <p class="hello">{% call "app:say_hello" request.user %}</p>


        This would output something like:

        <p class="hello">Hello, Dirley Rodrigues!</p>
    """

    # FIXME Theres probably something in Django that already does this.
    if ':' in helper:
        app, helper = helper.split(':', 1)
    else:
        app = None

    if app is not None:
        apps = [django_apps.get_app_config(app)]
    else:
        apps = django_apps.get_app_configs()

    filter_func = None
    for app in apps:
        if module_has_submodule(app.module, HELPERS_MODULE_NAME):
            helpers_module_name = '{0}.{1}'.format(app.name, HELPERS_MODULE_NAME)
            helpers_module = import_module(helpers_module_name)
            filter_func = getattr(helpers_module, helper)
            if filter_func is not None:
                break

    assert filter_func, NameError("Couldn't find a helper named '{0}'".format(helper))

    return filter_func(context, *args, **kwargs)
