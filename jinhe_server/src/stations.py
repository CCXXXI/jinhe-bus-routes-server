from flask import Blueprint, jsonify
from redisgraph import Node

from . import g, r

bp = Blueprint("stations", __name__, url_prefix="/stations")


@bp.route("/")
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


@bp.route("/<id_>/first")
def stations_id_first(id_):
    """The first service of the station."""
    return jsonify(
        [
            (n.removeprefix("_"), t)
            for n, t in r.zrange(f"Station:_{id_}:first", 0, -1, withscores=True)
        ]
    )
