from flask import Blueprint, jsonify

from . import r

bp = Blueprint("routes", __name__, url_prefix="/routes")


@bp.route("/")
def routes():
    """All routes name and directional."""
    return {n.removeprefix("_"): d for n, d in r.hgetall("Routes").items()}


@bp.route("/<name>")
def routes_name(name: str):
    """The basic info of the route."""
    return r.hgetall(f"Route:_{name}")


@bp.route("/<name>/first")
def routes_name_first(name: str):
    """The first service of the route."""
    return jsonify(
        [
            (i.removeprefix("_"), t)
            for i, t in r.zrange(f"Route:_{name}:first", 0, -1, withscores=True)
        ]
    )
