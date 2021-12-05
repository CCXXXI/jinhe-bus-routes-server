from flask import Blueprint, jsonify

from . import cached, g

bp = Blueprint("stats", __name__, url_prefix="/stats")


@bp.route("/stations/most-routes")
@cached()
def stations_most_routes():
    """The 15 stations with most routes."""
    return jsonify(
        [
            [s.removeprefix("_"), c, [r.removeprefix("_") for r in rs]]
            for s, c, rs in g.query(
                "MATCH (p)-[r]-() "
                "RETURN labels(p), count(distinct type(r)), collect(distinct type(r)) "
                "ORDER BY count(type(r)) desc "
                "LIMIT 15",
                read_only=True,
            ).result_set
        ]
    )
