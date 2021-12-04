import logging

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from .db import get_db

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


def register_blueprints():
    """Register all blueprints."""
    from . import meta, routes, stations

    app.register_blueprint(meta.bp)
    app.register_blueprint(routes.bp)
    app.register_blueprint(stations.bp)


with app.app_context():
    r, g = get_db()
register_blueprints()
