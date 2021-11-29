import logging

import sentry_sdk
from flask import Flask
from redis import Redis
from redisgraph import Graph
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://a7ad189559a44dd8819c0862367ecbfe@o996799.ingest.sentry.io/6042882",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

r = Redis(decode_responses=True)
g = Graph("g", r)

app = Flask(__name__)


@app.route("/version")
def version():
    """The Git commit ID of the data."""
    return r.get("version")


@app.route("/route/<name>")
def route(name: str):
    """The basic info of the route."""
    return r.hgetall(f"Route:{name}")
