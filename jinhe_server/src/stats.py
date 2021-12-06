from flask import Blueprint, jsonify

from . import cached, g, r

bp = Blueprint("stats", __name__, url_prefix="/stats")


@bp.route("/routes/types")
@cached()
def routes_types():
    """The types of routes."""
    return {t: int(c) for t, c in r.hgetall("Stats:Route.type").items()}


@bp.route("/routes/stations")
@cached()
def routes_stations():
    """The counts of stations of routes."""
    return jsonify(
        [
            (n.removeprefix("_"), int(c))
            for n, c in r.zrange(
                "Stats:Route.stations", 0, 14, desc=True, withscores=True
            )
        ]
    )


@bp.route("/routes/time")
@cached()
def routes_time():
    """The runtimes of routes."""
    return jsonify(
        [
            (n.removeprefix("_"), int(c))
            for n, c in r.zrange("Stats:Route.time", 0, 14, desc=True, withscores=True)
        ]
    )


@bp.route("/stations/routes")
@cached()
def stations_routes():
    """The 15 stations with most routes."""
    return jsonify(
        [
            [s.removeprefix("_"), c, [n.removeprefix("_") for n in rs]]
            for s, c, rs in g.query(
                "MATCH (p)-[r]-() "
                "RETURN labels(p), count(distinct type(r)), collect(distinct type(r)) "
                "ORDER BY count(type(r)) desc "
                "LIMIT 15",
                read_only=True,
            ).result_set
        ]
    )


@bp.route("/stations/links")
@cached()
def stations_links():
    """The links of stations."""
    return jsonify(
        g.query(
            "MATCH (a)-[r]->(b) "
            "WHERE a.en<>b.en "
            "RETURN a.zh, b.zh, count(r) "
            "ORDER BY count(r) desc "
            "LIMIT 15",
            read_only=True,
        ).result_set
    )
