"use strict";

const axios = require('axios')
const Vue = require('vue')
const Moment = require('moment')

import Bootstrap from 'bootstrap'
import BootstrapDatePicker from 'vue-bootstrap-datetimepicker'
import Multiselect from 'vue-multiselect'
import VueFormGenerator from "vue-form-generator";

import "vue-form-generator/dist/vfg.css"
import "vue-multiselect/dist/vue-multiselect.min.css"
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.css'

Vue.use({
    Bootstrap,
    BootstrapDatePicker,
    Moment,
    VueFormGenerator,
})


Vue.component('multiselect', Multiselect)
Vue.component('vue-form-generator', VueFormGenerator.component)

const SCHEMA_FORMAT = "vue-form-generator"
const SURVEY_API_URL = `/for_test_app/test-api/${definitionName}/`


if (definitionName) {
    vm = new Vue({
        el: "#app",
        components: {
            "vue-form-generator": VueFormGenerator.component,
            "multiselect": Multiselect
        },

        data: {
            model: {},
            schema: {
                fields: []
            },
            formOptions: {
                validateAfterLoad: false,
                validateAfterChanged: true
            },
            timerForPostValidation: null
        },

        methods: {
            setSchema: function(e) {
                function _setSchema(schemaData) {
                    for (let i in schemaData["fields"]) {
                        let field = schemaData["fields"][i]
                    }
                    return schemaData
                }
                let schemaUrl = SURVEY_API_URL + "?format=" + SCHEMA_FORMAT
                axios.get(schemaUrl, {}).then( response => {
                    let schemaData = _setSchema(response.data)

                    for (let schema of schemaData.fields){
                        schema["validator"].push(this.customValidator)
                    }

                    for (let schema of schemaData.fields) {
                        if (schema.type == "dateTimePicker") {
                            schema["onChanged"] = function(model, newVal, oldVal, field) {
                                let format = field.dateTimePickerOptions.format
                                let result = Moment(newVal).format(format)

                                if (result != "Invalid date") {
                                    model[field.model] = Moment(newVal).format(format)
                                } else {
                                    model[field.model] = newVal
                                }
                            }
                        }
                    }

                    this.schema = schemaData

                    // TODO:既に入力があった場合はそっちをMergeする
                    let defaultModel = {}
                    for (let fieldSchema of this.schema.fields) {
                        defaultModel[fieldSchema.model] = null
                    }

                    let newModel = VueFormGenerator.schema.createDefaultObject(this.schema, defaultModel);

                    this.model = newModel
                })
            },

            preparePostData: function() {
                let postData = Object.assign({}, this.model)
                for (let fieldSchema of this.schema.fields) {
                    if (fieldSchema.type === "vueMultiSelect") {
                        let modelName = fieldSchema.model
                        let modelData = this.model[modelName]
                        let selectOption = fieldSchema.selectOptions || {}

                        if (selectOption.multiple == true) {
                            postData[modelName] = new Array()
                            for (let data of modelData){ postData[modelName].push(data.id) }
                        } else {
                            postData[modelName] = modelData["id"] || []
                        }
                    }
                }
                return postData
            },

            customValidator: function(value, field) {

                var postData = this.preparePostData()

                if (this.timerForPostValidation !== null) {
                    clearTimeout(this.timerForPostValidation)
                }

                return new Promise((resolve, reject) => {
                    this.timerForPostValidation = setTimeout(() => {
                        var _field = field
                        axios.post(SURVEY_API_URL, postData)
                        .then(
                            function(response) {resolve()}.bind(this)
                        ).catch(
                            function(error) {
                                resolve(error.response.data[_field.model]);
                            }.bind(this)
                        );
                    }, 400);
                });

            },

            postData: function() {
                let postData = this.preparePostData()
                axios.post(SURVEY_API_URL, postData)
                    .then(
                        function(res) {
                            console.log(res)
                        }
                        // } .bind(this)
                    ).catch(
                        function(err) {
                            console.log(err)
                        }
                        // .bind(this)
                    );
            },

            prettyJSON: function(json) {
                if (json) {
                    json = JSON.stringify(json, undefined, 4);
                    json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
                    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
                        var cls = 'number';
                        if (/^"/.test(match)) {
                            if (/:$/.test(match)) {
                                cls = 'key';
                            } else {
                                cls = 'string';
                            }
                        } else if (/true|false/.test(match)) {
                            cls = 'boolean';
                        } else if (/null/.test(match)) {
                            cls = 'null';
                        }
                        return '<span class="' + cls + '">' + match + '</span>';
                    });
                }
            }
        },
        created: function() {
            this.setSchema()
        }
    });
}
