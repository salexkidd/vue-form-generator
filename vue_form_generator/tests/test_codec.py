from django.test import TestCase, override_settings, modify_settings

from ..codec import VueFormGeneratorEncoder

from definable_serializer.serializers import build_serializer_by_yaml_file

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


DEFINITION_FILES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "serializer_definitions")


class TestBase(TestCase):
    def setUp(self):
        options = Options()

        # Chromeのパス（Stableチャネルで--headlessが使えるようになったら不要なはず）
        # options.binary_location = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'

        # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
        options.add_argument('--headless')

        # ChromeのWebDriverオブジェクトを作成する。
        self.driver = webdriver.Chrome(chrome_options=options)

    def tearDown(self):
        self.driver.quit()

    def _load_definition_file(self, filename):
        return build_serializer_by_yaml_file(
            os.path.join(DEFINITION_FILES_DIR, filename))


class TestCodec(TestBase):

    def test_all_field(self):
        serializer_class = self._load_definition_file("all_field.yml")
        serializer = serializer_class()
        encoder = VueFormGeneratorEncoder(serializer)
        schema = encoder.get_vue_form_generators_schema()

    def test_external_field(self):
        serializer_class = self._load_definition_file("external_field.yml")
        serializer = serializer_class()
        encoder = VueFormGeneratorEncoder(serializer)
        schema = encoder.get_vue_form_generators_schema()


class WebTest(TestBase):
    def test_chrome(self):
        self.driver.get('https://www.google.co.jp/')
        assert 'Google' in self.driver.title
