from django.test import TestCase
from core import utils


class UtilsTestCase(TestCase):

    def test_reference_filename(self):
        output = utils.references_filename(None, 'Test FileNAME.py')
        self.assertEquals(output, 'bill/references/test-filename.py')

    def test_theme_icon_filename(self):
        output = utils.theme_icon_filename(None, 'Test FileNAME.png')
        self.assertEquals(output, 'bill/themes/test-filename.png')
