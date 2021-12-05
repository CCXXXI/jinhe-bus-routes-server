import logging

import sentry_sdk
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

from .db import get_db, get_redis_host

sentry_sdk.init(
    dsn="https://a7ad189559a44dd8819c0862367ecbfe@o996799.ingest.sentry.io/6042882",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(
    Response(status=404),
    {"/jinhe": app.wsgi_app},
)
CORS(app)
_cache = Cache(
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 0,  # never expires
        "CACHE_KEY_PREFIX": "Cache:",
        "CACHE_REDIS_HOST": get_redis_host(),
    }
)
_cache.init_app(app)

cached = _cache.cached

with app.app_context():
    r, g = get_db()


def _register_blueprints():
    """Register all blueprints."""
    from . import meta, routes, stations

    app.register_blueprint(meta.bp)
    app.register_blueprint(routes.bp)
    app.register_blueprint(stations.bp)


_register_blueprints()
