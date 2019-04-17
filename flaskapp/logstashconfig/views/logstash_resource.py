from flask.views import MethodView
from flask import jsonify
from flask import request
from flaskapp.extensions.api import api
from flaskapp.logstashconfig.views.blueprint import logstashconfig
from flaskapp.logstashconfig.views.example_conf import patient_conf
from jinja2 import Template
import os

es_host = os.environ.get('ES_HOST', 'http://elasticsearch:9200')


class FHIRLogstashConfigAPI(MethodView):

    def _render_pipeline(self, context):
        table_name = context.get('table_name')
        primary_key = context.get('primary_key')
        resource_type = context.get('resourceType', '').lower()

        # TODO: validation?

        # Remove empty fields config
        suspected_fields = "SuspectFields = {suspected_fields}"
        sanitize_columns = [c.lower() for c in
                            context.get('sanitize_columns', [])]
        sanitize_columns = suspected_fields.format(
            suspected_fields=sanitize_columns)

        # MAIN TABLE SELECT
        sqlstatement = f"SELECT * FROM {table_name} t"
        # JOIN TABLE STATEMENTS
        for i, join in enumerate(context.get('joins', [])):
            sqlstatement += f' LEFT JOIN {join["table_name"]} t{i} on t{i}.{join["key"]} = t.{primary_key}'

        # START FILTER
        logstash_filter = """"""
        for fields in context.get('fields_mappings', []):
            logstash_mapping_field = fields.get('logstash_field')
            db_column = fields.get('db_column', '').lower()
            data_type = fields.get('column_type', 'string')
            use = fields.get('use')
            use_mutate = ""
            if use:
                use_mutate = f"""mutate {{ add_field => {{ "{logstash_mapping_field}[use]" => "{use}" }} }}"""

            if data_type == 'date' or data_type == 'datetime':
                # TODO: implement datetime
                pass
            else:
                logstash_filter += f"""
    if [{db_column}] {{
        mutate {{ rename => {{ "[{db_column}]" => "{logstash_mapping_field}" }}}}
        {use_mutate}
    }}
                """
        # END FILTER
        # logstash_filter += """}"""

        with open('logstash/config_generator/pipeline.template.conf',
                  'r') as template_file:
            tm = Template(template_file.read())
            msg = tm.render(connection=f'{context["host"]}:{context["port"]}',
                            username=context['username'],
                            password=context['password'],
                            database=f"{context['host']}:{context['port']}",
                            mutate_query=logstash_filter,
                            sqlstatement=sqlstatement,
                            sanitize_string=sanitize_columns,
                            resource_type=resource_type,
                            es_host=es_host
                            )
            return msg

    def get(self, _version, resource):
        example = request.args.get('example')

        if example:

            # Test endpoint for example configurations
            if resource == 'Patient':
                # return jsonify(self._render_pipeline(test_config))
                return jsonify(patient_conf)
            else:
                example_config = {
                    "host": "<host>",
                    "port": 1433,
                    "password": "<password>",
                    "username": "<username>",
                    "table_name": "<table>",
                    "primary_key": "<primary_key>",
                    "joins": [
                        {
                            "table_name": "<join_table_name>",
                            "key": "<join_table_key_column>"
                        }
                    ],
                    "fields_mappings": [
                        {
                            "field_name": "<field_name>",
                            "db_column": "<db_column>",
                            "logstash_field": "[<logstash_field>]",
                            "column_type": "<column_type>"
                        }
                    ]
                }

                return jsonify(example_config)
        else:
            with open(f'logstash/pipeline/pipeline.{resource.lower()}.conf',
                      'r') as f:
                return jsonify(f.read())

        # return jsonify(process_resource(resource))

    def post(self, _version, resource):
        configuration = request.get_json() or patient_conf

        logstash_pipeline = self._render_pipeline(configuration)
        with open(f'logstash/pipeline/pipeline.{resource.lower()}.conf',
                  'w+') as f:
            f.write(logstash_pipeline)

        # TODO: validation
        return jsonify(logstash_pipeline)

    def delete(self, _version, resource):
        try:
            os.remove(f'logstash/pipeline/pipeline.{resource.lower()}.conf')
        except Exception as e:
            pass

        return jsonify()


logstashconfig_view = FHIRLogstashConfigAPI.as_view('logstashconfig')

api.add_url_rule(
    logstashconfig.url_prefix + '/',
    view_func=logstashconfig_view,
    methods=['GET', 'POST', 'DELETE'],
    defaults={'resource': None}
)

api.add_url_rule(
    logstashconfig.url_prefix + '/<resource>',
    view_func=logstashconfig_view,
    methods=['GET', 'POST', 'DELETE'],
)
