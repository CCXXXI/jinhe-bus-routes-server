import logging

import sentry_sdk
from flask import Flask, jsonify
from redisgraph import Node
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
with app.app_context():
    r, g = get_db()


@app.route("/version")
def version():
    """The Git commit ID of the data."""
    return r.get("version")


@app.route("/routes/")
def routes():
    """All routes name and directional."""
    return {n.removeprefix("_"): d for n, d in r.hgetall("Routes").items()}


@app.route("/routes/<name>")
def routes_name(name: str):
    """The basic info of the route."""
    return r.hgetall(f"Route:_{name}")


@app.route("/stations/")
def stations():
    """All stations info."""
    res: list[Node] = [
        s[0] for s in g.query("MATCH (s) RETURN s", read_only=True).result_set
    ]
    return jsonify(
        [
            {"id": station.label.removeprefix("_")} | station.properties
            for station in res
        ]
    )


@app.route("/routes/<name>/first")
def routes_name_first(name: str):
    """The first service of the route."""
    return jsonify(
        [
            (s.removeprefix("_"), t)
            for s, t in r.zrange(f"Route:_{name}:first", 0, -1, withscores=True)
        ]
    )
