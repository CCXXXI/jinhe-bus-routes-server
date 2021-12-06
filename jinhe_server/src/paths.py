from collections import defaultdict
from heapq import heappop, heappush
from math import inf

from flask import Blueprint, jsonify

from . import cached, g

bp = Blueprint("paths", __name__, url_prefix="/paths")


@bp.route("/shortest/<u_raw>/<v_raw>")
@cached()
def shortest(u_raw, v_raw):
    """The shortest path between two groups of stations."""
    us = {"_" + u for u in u_raw.split(".")}
    vs = {"_" + v for v in v_raw.split(".")}
    d = defaultdict(lambda: inf)
    q = []
    pre = {}
    for u in us:
        d[u] = 0
        heappush(q, (0, u))
    while q:
        du, u = heappop(q)
        if u in vs:
            res = [u]
            while p := pre.get(u):
                res.extend(p)
                u = p[-1]
            return jsonify(
                tuple(
                    x.removeprefix("_") if isinstance(x, str) else x
                    for x in reversed(res)
                )
            )
        if du != d[u]:  # visited
            continue
        edges = g.query(
            f"MATCH (:{u})-[r]->(v) RETURN r.t, type(r), labels(v) ORDER BY r.t"
        ).result_set
        if p := pre.get(u):
            edges.sort(key=lambda e: (e[0], e[1] != p[1]))  # same type first
        for t, r, v in edges:
            if (dv := du + t) < d[v]:
                d[v] = dv
                heappush(q, (dv, v))
                pre[v] = (t, r, u)
    return jsonify([])  # no path
