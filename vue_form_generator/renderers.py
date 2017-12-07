from rest_framework.renderers import BaseRenderer
from rest_framework import status as http_status

from .codec import VueFormGeneratorEncoder

import json


class VueFormGeneratorSchemaRenderer(BaseRenderer):
    media_type = "application/vue-form-generator+json"
    format = "vue-form-generator"
    charset = 'utf-8'
    render_style = 'text'
    public = False

    def render(self, data, media_type=None, renderer_context=None):
        view = renderer_context["view"]
        request = renderer_context["request"]
        renderer_context["response"].status_code = http_status.HTTP_200_OK

        serializer_class = view.get_serializer_class()
        encoder = VueFormGeneratorEncoder(serializer_class())
        return json.dumps(
            encoder.get_vue_form_generator_schema(),
            ensure_ascii=False
        )
