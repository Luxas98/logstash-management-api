from flask.views import MethodView
from flaskapp.extensions.api import api
from flaskapp.docs.views.blueprint import docs
from flask import send_file
from werkzeug.utils import safe_join

print('Start')


class DocsAPI(MethodView):
    def get(self, _version, path):
        if '.png' in path:
            send_file(f'docs/views/docs/{path}', mimetype='image/png')

        return send_file(safe_join('docs/views/docs/',path))


docs_view = DocsAPI.as_view('docs')

api.add_url_rule(
    docs.url_prefix + '/<path:path>',
    view_func=docs_view,
    methods=['GET', 'POST', 'DELETE'],
)
