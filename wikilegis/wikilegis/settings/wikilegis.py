from importlib import import_module
from .. import settings

import pkgutil
import os

pkgpath = os.path.dirname(settings.__file__)
app = import_module('..application', package=__name__)

variables = globals()

for module_loader, name, ispkg in pkgutil.iter_modules([pkgpath]):
    module = import_module('..' + name, package=__name__)
    for var in dir(module):
        variables[var] = module.__dict__[var]

from core import plugins # noqa

plugins_dict = plugins.load_current_plugins()

for name, is_active in plugins_dict.items():
    if is_active:
        plugin_settings = plugins.get_settings(name)
        settings_variables = getattr(plugin_settings, 'SETTINGS_VARIABLES', {})
        for key, value in settings_variables.items():
            variables[key] = value
