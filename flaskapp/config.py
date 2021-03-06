import os
from gcloudlogging.logger import create_logger


log = create_logger()

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)

STATIC_FOLDER = os.environ.get(
    'FLASK_STATIC_FOLDER', os.path.join(PROJECT_ROOT, 'static')
)
STATIC_URL_PATH = '/static'  # serve asset files in static/ at /static/

API_BUNDLES = os.environ.get('ENDPOINTS', 'field').split(',')

if not API_BUNDLES:
    log.error(
        "Please specify which API bundle to use, available flaskapp: ['field'], "
        "eg. API_BUNDLES=field "
    )



# list of bundle modules to register with the app, in dot notation
BUNDLES = [f'flaskapp.{bundle}' for bundle in API_BUNDLES]

# ordered list of extensions to register before the bundles
# syntax is import.name.in.dot.module.notation:extension_instance_name
EXTENSIONS = [
    'flaskapp.extensions:session',
]

# list of extensions to register after the bundles
# syntax is import.name.in.dot.module.notation:extension_instance_name
DEFERRED_EXTENSIONS = [
    'flaskapp.extensions.api:api',
]

PROJECT_ID = 'project-id'


def get_boolean_env(name, default):
    default = 'true' if default else 'false'
    return os.getenv(name, default).lower() in ['true', 'yes', '1']


class BaseConfig(object):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    DEBUG = get_boolean_env('FLASK_DEBUG', False)
    STRICT_SLASHES = False
    BUNDLES = BUNDLES

    ##########################################################################
    # security                                                               #
    ##########################################################################
    # GCS - File handler
    ALLOWED_EXTENSIONS = ['dcm', 'stl', 'gz']

    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')  # TODO: FIXME
    # JWT_COOKIE_CSRF_PROTECT = False
    # JWT_TOKEN_LOCATION = ('headers', 'cookies', 'query_string', 'json')
    # JWT_QUERY_STRING_NAME = "jwt_token"
    # JWT_ACCESS_TOKEN_EXPIRES = False
    # JWT_ALGORITHM = 'RS256'
    # JWT_PUBLIC_KEY = 'RS256'
    # JWT_IDENTITY_CLAIM = 'sub'

    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False

    PROPAGATE_EXCEPTIONS = True


class ProdConfig(BaseConfig):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    ENV = 'prod'
    DEBUG = get_boolean_env('FLASK_DEBUG', False)


class DevConfig(BaseConfig):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    ENV = 'dev'
    DEBUG = get_boolean_env('FLASK_DEBUG', True)
    # EXPLAIN_TEMPLATE_LOADING = True

    ##########################################################################
    # session/cookies                                                        #
    ##########################################################################
    SESSION_COOKIE_SECURE = False

    WTF_CSRF_ENABLED = False


class TestConfig(BaseConfig):
    TESTING = True
    DEBUG = True

    WTF_CSRF_ENABLED = False
