from django.test import TestCase, override_settings, modify_settings

from ..codec import VueFormGeneratorEncoder

from definable_serializer.serializers import build_serializer_by_yaml_file

import os


DEFINITION_FILES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "serializer_definitions")


class TestBase(TestCase):

    def _load_definition_file(self, filename):
        return build_serializer_by_yaml_file(
            os.path.join(DEFINITION_FILES_DIR, filename))


class TestCodec(TestBase):

    def test_all_field(self):
        serializer_class = self._load_definition_file("all_field.yml")
        serializer = serializer_class()
        encoder = VueFormGeneratorEncoder(serializer)
        schema = encoder.get_vue_form_generator_schema()

    # def test_external_field(self):
    #     serializer_class = self._load_definition_file("external_field.yml")
    #     serializer = serializer_class()
    #     encoder = VueFormGeneratorEncoder(serializer)
    #     schema = encoder.get_vue_form_generator_schema()
