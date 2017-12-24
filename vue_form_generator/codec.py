from django.conf import settings as dj_settings
from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework.fields import empty

import pydoc
from copy import deepcopy

TIME_ONLY_FORMAT = "HH:mm:ss"
DATE_ONLY_FORMAT = "YYYY-MM-DD"
DATETIME_FORMAT = "YYYY-MM-DD HH:mm:ss"
UUID_REGEX = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


FIELD_AND_VUE_FORM_GENERATOR_MAP = {

    # boolean
    serializers.BooleanField:     {"type": "switch"},
    serializers.NullBooleanField: {"type": "switch"},

    # string
    serializers.CharField:  {"type": "input"},
    serializers.EmailField: {"type": "input", "validator": ["email"]},
    serializers.RegexField: {"type": "input", "validator": ["regexp"]},
    serializers.SlugField:  {"type": "input", "validator": ["regexp"]},
    serializers.URLField:   {"type": "input", "validator": ["url"]},
    serializers.UUIDField:  {
        "type": "input", "validator": ["regexp"], "pattern": UUID_REGEX
    },

    serializers.FilePathField:  {"type": "input"},
    serializers.IPAddressField: {"type": "input", "validator": ["string"]},

    # number
    serializers.IntegerField: {
        "type": "input", "inputType": "number", "validator": ["number"]
    },
    serializers.FloatField:   {"type": "input", "validator": ["number"]},
    serializers.DecimalField: {"type": "input", "validator": ["number"]},

    # date
    serializers.DateTimeField: {
        "type": "dateTimePicker",
        "validator": ["date"],
        "dateTimePickerOptions": {"format": DATETIME_FORMAT},
    },
    serializers.DateField: {
        "type": "dateTimePicker",
        "validator": ["date"],
        "dateTimePickerOptions": {"format": DATE_ONLY_FORMAT},
    },
    serializers.TimeField: {
        "type": "dateTimePicker",
        "validator": ["date"],
        "format": TIME_ONLY_FORMAT,
        "dateTimePickerOptions": {"format": TIME_ONLY_FORMAT},
    },
    serializers.DurationField: {"type": "input"},

    # Choices
    serializers.ChoiceField: {
        "type": "vueMultiSelect",
        "selectOptions": {"key": "name", "label": "name",}
    },

    serializers.MultipleChoiceField: {
        "type": "vueMultiSelect",
        "selectOptions": {
            "multiple": True,
            "trackBy": "name",
            "key": "name",
            "label": "name",
            "hideSelected": True,
        }
    },

    # Hidden Field
    serializers.HiddenField: {"type": "input", "inputType": "hidden",},
}

external_field_and_vue_form_generator_map = getattr(
    dj_settings, "VUE_FORM_GENERATOR_SETTINGS", {}
).get(
    "EXTERNAL_FIELD_AND_VUE_FORM_GENERATOR_MAP", {}
)

for class_path, value in external_field_and_vue_form_generator_map.items():
    FIELD_AND_VUE_FORM_GENERATOR_MAP.update(
        {pydoc.locate(class_path): value}
    )


DEFAULT_FIELD_AND_VUE_FORM_GENERATOR_MAP = {"type": "input"}


class VueFormGeneratorEncoder:

    def __init__(self, serializer):
        self._serializer = serializer

    def _prepare_validatorand_insert_required(self, field, data):
        if not "validator" in data:
            data["validator"] = list()

        data["validator"] = list()
        # if field.required:
        #     data["validator"].append("required")

    def _set_input_max_length(self, field, data):
        if data["type"] == "input":
            max_length = getattr(field, "max_length", None)

            if max_length:
                data["maxlength"] = max_length

    def _set_number_min_and_max(self, field, data):
        if data.get("inputType", None) == "number":
            data["max"] = field.max_value
            data["min"] = field.min_value

    def _set_regex_expression_if_using_regex_validator(self, field, data):
        if "regexp" not in data["validator"]:
            return

        pattern = None
        for validator in field.validators:
            if isinstance(validator, RegexValidator):
                pattern = validator.regex.pattern
                break

        if pattern:
            pattern = pattern.encode('unicode-escape').decode("utf-8")
            data["pattern"] = pattern

    def _set_select_values(self, field, data):

        if data["type"] in ("radios", "checklist",):
            data["styleClasses"] = ["vfg-radio-class"]
            data["values"] = [
                {"name": label, "value": value}
                    for value, label in field.choices.items()
            ]

        elif data["type"] in ("vueMultiSelect",):
            data["values"] = []
            for value, label in field.choices.items():
                if not value:
                    data["selectOptions"]["noneSelectedText"] = label
                else:
                    data["values"].append({"name": label, "id": value})

            # set ID to select input box
            data["selectOptions"]["id"] = field.field_name


    def _set_default(self, field, data):
        if not field.initial:
            return

        def _default_value(value):
            return {"name": field.choices.get(value, ""), "id": value}

        if data["type"] in ("vueMultiSelect",):
            if data.get("selectOptions", {}).get("multiple", False):
                data["default"] = list()
                for value in field.initial:
                    data["default"].append(_default_value(value))
            else:
                data["default"] = _default_value(field.initial)

        elif data["type"] in ("dateTimePicker",):
            data["default"] = field.initial.isoformat()

        else:
            data["default"] = field.initial

    def set_field_label_and_hint(self, field, data):
        label = ""
        hint = ""

        if not isinstance(field, serializers.HiddenField):
            label = field.label
            hint = field.help_text

        data["label"] = label
        data["hint"] = hint


    def _build_schema(self, field):
        data = deepcopy(
            FIELD_AND_VUE_FORM_GENERATOR_MAP.get(
                field.__class__, DEFAULT_FIELD_AND_VUE_FORM_GENERATOR_MAP)
        )

        self.set_field_label_and_hint(field, data)
        self._prepare_validatorand_insert_required(field, data)
        self._set_input_max_length(field, data)
        self._set_number_min_and_max(field, data)
        self._set_regex_expression_if_using_regex_validator(field, data)
        self._set_select_values(field, data)
        self._set_default(field, data)

        return data

    def get_vue_form_generator_schema(self):
        result = {"fields": []}
        for field_name, field in self._serializer.fields.items():
            field_data = {
                "id": field_name,
                "model": field_name,
                "required": field.required,
                "readonly": field.read_only,
            }
            field_data.update(self._build_schema(field))
            result["fields"].append(field_data)


        return result
