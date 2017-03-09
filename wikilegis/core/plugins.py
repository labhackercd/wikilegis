import json
import os
import pkgutil

import click
from django.conf import settings
import importlib
import pip


PLUGINS_CONFIG_FILE = settings.BASE_DIR + '/.plugins'


def create_config_file():
    if not os.path.exists(PLUGINS_CONFIG_FILE):
        os.mknod(PLUGINS_CONFIG_FILE)
        for _, name, _ in pkgutil.iter_modules(['plugins']):
            remove_plugin(name)
        return True
    else:
        return False


def load_current_plugins():
    create_config_file()
    config_file = open(PLUGINS_CONFIG_FILE, 'r')
    plugins_json = config_file.read()
    config_file.close()

    if plugins_json:
        plugins_dict = json.loads(plugins_json)
    else:
        plugins_dict = {}
    return plugins_dict


def write_config_file(plugins_dict):
    config_file = open(PLUGINS_CONFIG_FILE, 'w')
    config_file.seek(0)
    config_file.truncate()
    config_file.write(json.dumps(plugins_dict, indent=2, sort_keys=True))
    config_file.close()


def add_plugin(plugin_name):
    plugins_dict = load_current_plugins()
    plugins_dict[plugin_name] = True

    plugin_settings = get_settings(plugin_name)
    click.secho('Installing dependencies', bold=True)

    for dependency in plugin_settings.DEPENDENCIES:
        pip.main(['install', dependency])

    write_config_file(plugins_dict)


def get_settings(plugin_name):
    settings_path = 'plugins.{}.settings'.format(plugin_name)
    return importlib.import_module(settings_path)


def remove_plugin(plugin_name):
    plugins_dict = load_current_plugins()
    plugins_dict[plugin_name] = False

    write_config_file(plugins_dict)
