import click
from jinja2 import Template



def render_pipeline(context):
    table_name = context.get('table_name')

    sqlstatement = f"SELECT * FROM {table_name} t"
    # TODO: validation

    for fields in context.get('fields_mappings', []):
        logstash_mapping_field = fields.get('logstash_field')
        db_column = fields.get('db_column')


    with open('pipeline.template.conf', 'r') as template_file:
        tm = Template(template_file.read())
        msg = tm.render(connection=f'{context["host"]}:{context["port"]}',
                        username=context['username'],
                        password=context['password'],
                        database=context['database']
                        )
        return msg

@click.command()
@click.option('--host', default="mssql", help='MSSQL Hostname', prompt='Host')
@click.option('--port', default=1433, help='MSSQL Port', prompt='Port')
@click.option('--database', help='MSSQL to load database', prompt='Database')
@click.option('--username', help='MSSQL user', prompt='User')
@click.option('--password', help='MSSQL user password', prompt='Password')
def generate_template(host, port, database, username, password):
    print(f'Connection {host}:{port}')
    print(f'Database {database}')
    print(f'Username {username}')
    print(f'Password {password}')

    print(render_pipeline({
        "host": host,
        "port": port,
        "database": database,
        "username": username,
        "password": password
    }))





if __name__ == '__main__':
    generate_template()
