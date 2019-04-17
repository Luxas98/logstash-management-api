import os
from flaskapp.api import Api
# Flask-Restful must be initialized _AFTER_ the SQLAlchemy extension has
# been initialized, AND after all views, models, and serializers have
# been imported. This is because the @api decorators create deferred
# registrations that depend upon said dependencies having all been
# completed before Api('api').init_app() gets called

api_route = os.environ.get('API_ROUTE')

api_url = f"/api/<_version>"

if api_route:
    api_url = f"{api_url}/{api_route}"

api = Api('api', prefix=api_url)
