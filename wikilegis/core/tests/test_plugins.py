from core import plugins
from django.test import TestCase
import mock


class PluginsTestCase(TestCase):

    @mock.patch('pkgutil.iter_modules')
    @mock.patch('os.path.exists')
    @mock.patch('os.mknod')
    def test_create_config_file(self, mock_mknod, mock_exists, mock_pkgutil):
        mock_exists.side_effect = [False, True]
        mock_pkgutil.return_value = [('', 'plugin_test', '', )]
        return_value = plugins.create_config_file()
        mock_exists.assert_called()
        mock_pkgutil.assert_called()
        mock_mknod.assert_called_with(plugins.PLUGINS_CONFIG_FILE)
        self.assertTrue(return_value)

    @mock.patch('os.path.exists')
    @mock.patch('os.mknod')
    def test_create_config_file_already_exists(self, mock_mknod, mock_exists):
        mock_exists.return_value = True
        return_value = plugins.create_config_file()
        mock_exists.assert_called()
        self.assertFalse(mock_mknod.called)
        self.assertFalse(return_value)

    @mock.patch('builtins.open', create=True)
    def test_load_current_plugins(self, mock_open):
        mock_open.side_effect = [
            mock.mock_open(read_data='').return_value
        ]
        self.assertEquals(plugins.load_current_plugins(), {})

    @mock.patch('builtins.open', create=True)
    def test_load_current_plugins_with_plugins_activated(self, mock_open):
        mock_open.side_effect = [
            mock.mock_open(read_data='{"plugin_test": false}').return_value
        ]
        self.assertEquals(plugins.load_current_plugins(),
                          {'plugin_test': False})

    @mock.patch('core.plugins.get_settings')
    @mock.patch('builtins.open', create=True)
    def test_add_plugin(self, mock_open, mock_settings):
        settings = mock.MagicMock()
        settings.DEPENDENCIES = []
        mock_settings.return_value = settings
        mock_open.return_value = mock.mock_open(
            read_data='{"plugin_test": false}'
        ).return_value
        plugins.add_plugin('plugin_test')
        mock_open.assert_called()
        mock_settings.assert_called_with('plugin_test')

    @mock.patch('core.plugins.get_settings')
    @mock.patch('builtins.open', create=True)
    def test_add_plugin_without_deps(self, mock_open, mock_settings):
        settings = mock.MagicMock()
        mock_settings.return_value = settings
        mock_open.return_value = mock.mock_open(
            read_data='{"plugin_test": false}'
        ).return_value
        plugins.add_plugin('plugin_test')
        mock_open.assert_called()
        mock_settings.assert_called_with('plugin_test')

    @mock.patch('core.plugins.get_installed_packages')
    @mock.patch('pip.main')
    @mock.patch('core.plugins.get_settings')
    @mock.patch('builtins.open', create=True)
    def test_add_plugin_with_deps(self, mock_open, mock_settings,
                                  mock_pip, mock_packages):
        settings = mock.MagicMock()
        settings.DEPENDENCIES = ['dep1']
        mock_packages.return_value = []
        mock_settings.return_value = settings
        mock_open.return_value = mock.mock_open(
            read_data='{"plugin_test": false}'
        ).return_value
        plugins.add_plugin('plugin_test')
        mock_open.assert_called()
        mock_settings.assert_called_with('plugin_test')
        mock_pip.assert_called_with(['install', 'dep1'])

    @mock.patch('core.plugins.get_installed_packages')
    @mock.patch('pip.main')
    @mock.patch('core.plugins.get_settings')
    @mock.patch('builtins.open', create=True)
    def test_add_plugin_dep_already_installed(self, mock_open, mock_settings,
                                              mock_pip, mock_packages):
        settings = mock.MagicMock()
        settings.DEPENDENCIES = ['dep1']
        mock_packages.return_value = ['dep1']
        mock_settings.return_value = settings
        mock_open.return_value = mock.mock_open(
            read_data='{"plugin_test": false}'
        ).return_value
        plugins.add_plugin('plugin_test')
        mock_open.assert_called()
        mock_settings.assert_called_with('plugin_test')
        self.assertFalse(mock_pip.called)

    @mock.patch('pip.get_installed_distributions')
    def test_get_installed_packages(self, mock_pip):
        package = mock.MagicMock()
        package.project_name = 'project_name'
        mock_pip.return_value = [package]
        self.assertEquals(plugins.get_installed_packages(), ['project_name'])

    @mock.patch('importlib.import_module')
    def test_get_settings(self, mock_importlib):
        plugins.get_settings('plugin_name')
        mock_importlib.assert_called_with('plugins.plugin_name.settings')
