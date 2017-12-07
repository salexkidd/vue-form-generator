"use strict";

const axios = require('axios')
const Vue = require('vue')

import Bootstrap from 'bootstrap'
import BootstrapDatePicker from 'vue-bootstrap-datetimepicker'
import Multiselect from 'vue-multiselect'
import Moment from 'moment'
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

const VUE_FORM_GENERATOR_SCHEMA_API_URL = `/for_test_app/test-api/${definitionName}/?format=vue-form-generator`
const SURVEY_API_URL = `/for_test_app/test-api/${definitionName}/?format=vue-form-generator`

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
            }
        },

        methods: {
            setSchema: function(e) {

                function _setSchema(schemaData) {
                    for (let i in schemaData["fields"]) {
                        let field = schemaData["fields"][i]
                    }
                    return schemaData
                }

                axios.get(VUE_FORM_GENERATOR_SCHEMA_API_URL, {}).then( response => {
                    let schemaData = _setSchema(response.data)
                    this.schema = schemaData


                    // 既に入力があった場合はそっちをMergeする
                    let newModel = VueFormGenerator.schema.createDefaultObject(this.schema, {});

                    this.model = newModel

                })
            },

            clearAllModelData: function() {
                this.model = {}
            },

            setNullAllModel: function() {
                let data = {}
                for (let k in this.model) {
                    data[k] = ""
                }
                let newModel = VueFormGenerator.schema.createDefaultObject(this.schema, data);
                this.model = newModel
                console.log(data)
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
