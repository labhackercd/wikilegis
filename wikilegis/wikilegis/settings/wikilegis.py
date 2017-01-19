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
