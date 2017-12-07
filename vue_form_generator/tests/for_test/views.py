from django.views.generic import TemplateView
from django.http import Http404

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from definable_serializer.serializers import build_serializer_by_yaml_file

import os

DEFINITION_FILES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "serializer_definitions",
)

API_SERIALIZER_DEFINITION_MAP = {
    "all_field": "all_field.yml",
    "multiple_select": "multiple_select.yml",
}


class TestForAllFieldView(TemplateView):
    template_name = "test.html"


class TestAPI(GenericAPIView):

    def _load_definition_file(self, definition):
        filename = API_SERIALIZER_DEFINITION_MAP.get(definition, "")
        filepath = os.path.join(
            DEFINITION_FILES_DIR, os.path.basename(filename))

        if not os.path.isfile(filepath):
            raise Http404("Not Found")

        return build_serializer_by_yaml_file(filepath)

    def get_serializer_class(self, *args, **kwargs):
        return self._load_definition_file(self.kwargs["definition"])

    def get(self, request, *args, **kwargs):
        return Response("OK")

    def post(self, request, *args, **kwargs):
        return Response("OK")
