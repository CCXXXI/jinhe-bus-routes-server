from flask import Blueprint, jsonify

from . import cached, r

bp = Blueprint("routes", __name__, url_prefix="/routes")


@bp.route("/")
@cached()
def index():
    """All routes name and directional."""
    return {n.removeprefix("_"): d for n, d in r.hgetall("Routes").items()}


@bp.route("/<name>")
@cached()
def info(name: str):
    """The basic info of the route."""
    return r.hgetall(f"Route:_{name}")


@bp.route("/<name>/first")
@cached()
def first(name: str):
    """The first service of the route."""
    return jsonify(
        [
            (i.removeprefix("_"), t)
            for i, t in r.zrange(f"Route:_{name}:first", 0, -1, withscores=True)
        ]
    )


@bp.route("/<name>/steps")
@cached()
def steps(name: str):
    """The service steps of the route."""
    return jsonify(sorted(map(int, r.smembers(f"Route:_{name}:steps"))))
