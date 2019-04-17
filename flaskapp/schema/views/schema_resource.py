from flask import request, jsonify
from flask.views import MethodView
from flaskapp.extensions.api import api
from flaskapp.schema.views.blueprint import schema
import pyodbc


class SchemaAPI(MethodView):

    def get(self, _version):
        host = request.args.get('host', 'localhost')
        database = request.args.get('database')
        password = request.args.get('password')
        table = request.args.get('table')

        conn = pyodbc.connect(
            'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
            f'Server={host};'
            f'Database={database};'
            f'uid=sa;pwd={password}')
        tables = []
        if not table:
            table_list_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"

            with conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(table_list_query)
                    tables = [row[0] for row in cursor.fetchall()]
                except pyodbc.ProgrammingError as e:
                    print(e)
                    print(f'Could not fetch tables fom DB {database}')
        else:
            tables.append(table)

        db_schema = {}
        for table_name in tables:
            query = f"SELECT t.* FROM {table_name} t"
            column_names = []
            with conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    cursor.fetchall()
                    column_names = [column[0] for column in cursor.description]
                except pyodbc.ProgrammingError as e:
                    print(e)
                    print('Already exists??')

                db_schema[table_name] = column_names

        return jsonify(db_schema)


schema_view = SchemaAPI.as_view('schema')

api.add_url_rule(
    schema.url_prefix,
    view_func=schema_view,
    methods=['GET'],
)

api.add_url_rule(
    schema.url_prefix + '/',
    view_func=schema_view,
    methods=['GET'],
)
