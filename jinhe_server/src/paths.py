from flask import Blueprint
from redisgraph import Path

from . import cached, g

bp = Blueprint("paths", __name__, url_prefix="/paths")


# WARNING: `shortestPath` may crash RedisGraph
# todo: wait for https://github.com/RedisGraph/RedisGraph/pull/2016
@bp.route("/shortest/<u>/<v>")
@cached()
def shortest(u, v):
    """The shortest path between two stations."""
    p: Path = g.query(
        f"MATCH (u:_{u}), (v:_{v}) RETURN shortestPath((u)-[*]->(v))",
        read_only=True,
    ).result_set[0][0]
    return {
        "s": [s.label.removeprefix("_") for s in p.nodes()],
        "r": [r.relation.removeprefix("_") for r in p.edges()],
    }
