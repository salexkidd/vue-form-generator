from django.test import (
    TestCase, override_settings, modify_settings
)
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from rest_framework import serializers

from definable_serializer.serializers import build_serializer_by_yaml_file
from definable_serializer import extra_fields

import os
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

DEFINITION_FILES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "serializer_definitions")


class LoadSerializerDefinitionMixin:

    def _load_definition_file(self, filename):
        return build_serializer_by_yaml_file(
            os.path.join(DEFINITION_FILES_DIR, filename))


class ChromeWebDriverMixin(TestCase):

    def setUpChromeWebDriver(self):
        options = Options()
        options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        options.add_argument('--headless')
        options.add_argument('--window-size=1900,1200')
        self.chrome_driver = webdriver.Chrome(chrome_options=options)

    def tearDownChromeWebDriver(self):
        self.chrome_driver.quit()

    def fullpage_screenshot(self, file):
        print("Starting chrome full page screenshot workaround ...")

        total_width = self.chrome_driver.execute_script("return document.body.offsetWidth")
        total_height = self.chrome_driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = self.chrome_driver.execute_script("return document.body.clientWidth")
        viewport_height = self.chrome_driver.execute_script("return window.innerHeight")
        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                self.chrome_driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(0.2)

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))

            self.chrome_driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        print("Finishing chrome full page screenshot workaround...")
        return True


class RendererTest(LoadSerializerDefinitionMixin,
                   ChromeWebDriverMixin,
                   StaticLiveServerTestCase):

    def setUp(self):
        self.setUpChromeWebDriver()

    def tearDown(self):
        self.tearDownChromeWebDriver()

    def test_datetime_initial_value_check(self):
        serialier_class = self._load_definition_file("all_field.yml")
        serializer = serialier_class()

        self.chrome_driver.get('{}/for_test_app/test-page/all_field/'.format(self.live_server_url))
        self.chrome_driver.implicitly_wait(0.5)

        target_field_classes = (
            serializers.DateTimeField,
            serializers.DateField,
            serializers.TimeField,
        )

        for field_name, field in serializer.fields.items():
            if not any([isinstance(field, k) for k in target_field_classes]):
                continue

            initial = field.initial
            if hasattr(initial, "tzinfo"):
                initial = initial.replace(tzinfo=None)

            initial = str(initial).replace("-", "/")
            element = self.chrome_driver.find_element_by_id(field_name)
            self.assertEqual(str(element.get_attribute("value")), initial)

    def test_input_initial_value_check(self):
        serialier_class = self._load_definition_file("all_field.yml")
        serializer = serialier_class()

        self.chrome_driver.get('{}/for_test_app/test-page/all_field/'.format(self.live_server_url))
        self.chrome_driver.implicitly_wait(0.5)

        target_field_classes = (
            serializers.CharField, serializers.EmailField,
            serializers.RegexField, serializers.SlugField,
            serializers.URLField, serializers.UUIDField,
            serializers.IntegerField, serializers.DecimalField,
            serializers.ReadOnlyField, serializers.HiddenField,
        )

        for field_name, field in serializer.fields.items():
            if not any([isinstance(field, k) for k in target_field_classes]):
                continue

            element = self.chrome_driver.find_element_by_id(field_name)
            self.assertEqual(str(element.get_attribute("value")), str(field.initial))

    def test_select_initial_value_check(self):
        target_class = serializers.ChoiceField

        serialier_class = self._load_definition_file("all_field.yml")
        serializer = serialier_class()

        self.chrome_driver.get('{}/for_test_app/test-page/all_field/'.format(self.live_server_url))
        self.chrome_driver.implicitly_wait(0.5)

        for field_name, field in serializer.fields.items():
            if field.__class__ == target_class:
                element = self.chrome_driver.find_element_by_id(field_name)
                self.assertEqual(
                    str(element.get_attribute("_value")),
                    field.choices[field.initial]
                )

    def test_multipleselect_initial_value_check(self):
        target_class = serializers.MultipleChoiceField

        serialier_class = self._load_definition_file("multiple_select.yml")
        serializer = serialier_class()

        self.chrome_driver.get('{}/for_test_app/test-page/all_field/'.format(self.live_server_url))
        self.chrome_driver.implicitly_wait(0.5)

        for field_name, field in serializer.fields.items():
            if field.__class__ == target_class:
                for element in self.chrome_driver.find_elements_by_xpath("//span[contains(@class, 'multiselect__tag')]"):
                    label_element = element.find_element_by_tag_name("span")
                    self.assertIn(
                        label_element.get_attribute("innerHTML"),
                        [field.choices.get(i) for i in field.initial]
                    )

    def test_radio_initial_value_check(self):
        target_class = extra_fields.RadioField

        serialier_class = self._load_definition_file("all_field.yml")
        serializer = serialier_class()

        self.chrome_driver.get('{}/for_test_app/test-page/all_field/'.format(self.live_server_url))
        self.chrome_driver.implicitly_wait(0.5)

        for field_name, field in serializer.fields.items():
            if field.__class__ == target_class:
                radio_list = self.chrome_driver.find_element_by_class_name("radio-list")
                selected_radio_input = radio_list.find_element_by_class_name("is-checked").find_element_by_tag_name("input")
                self.assertEqual(
                    field.initial,
                    selected_radio_input.get_attribute("value")
                )
