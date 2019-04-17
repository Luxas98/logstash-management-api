from flask.views import MethodView
from flask import jsonify
from flask import request
from flaskapp.extensions.api import api
from flaskapp.field.views.blueprint import field
from logstash.config_generator.fields_generator import process_resource


class FHIRFieldAPI(MethodView):
    def get(self, _version, resource):
        return jsonify(process_resource(resource))


field_view = FHIRFieldAPI.as_view('field')

api.add_url_rule(
    field.url_prefix + '/<resource>',
    view_func=field_view,
    methods=['GET'],
)
