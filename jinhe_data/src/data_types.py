from dataclasses import dataclass
from itertools import pairwise

from redis import Redis
from redisgraph import Edge, Graph, Node


@dataclass
class Route:
    """路线"""

    directional: bool
    """无向为false，不仅仅是环线，还有G62路等单向线路"""

    interval: int
    """班次间隔（分钟）"""

    kilometer: float
    """单向里程（公里）"""

    name: str
    """线路名"""

    oneway: str
    """运行时⻓"""

    route: str
    """线路走向"""

    runtime: str
    """运营时间，和班次表有略微不一致"""

    type: str
    """线路类型"""

    stations: tuple[int, ...] = None
    """不分上下行的沿线站点的 `id`"""

    services: tuple[tuple[str, ...], ...] = None
    """不分上下行的班次沿线站点时间"""

    up_stations: tuple[int, ...] = None
    """上行沿线站点的 `id`"""

    up_services: tuple[tuple[str, ...], ...] = None
    """上行班次沿线站点时间"""

    down_stations: tuple[int, ...] = None
    """下行沿线站点的 `id`"""

    down_services: tuple[tuple[str, ...], ...] = None
    """下行班次沿线站点时间"""

    def save(self, r: Redis, g: Graph):
        """Save self to the database."""
        # basic
        r.hset(
            f"Route:{self.name}",
            mapping={
                "directional": int(self.directional),
                "interval": self.interval,
                "kilometer": self.kilometer,
                "oneway": self.oneway,
                "route": self.route,
                "runtime": self.runtime,
                "type": self.type,
            },
        )

        # graph
        for s, d in (
            (self.stations, ""),
            (self.up_stations, "up"),
            (self.down_stations, "down"),
        ):
            if s:
                for u_id, v_id in pairwise(s):
                    u: Node = g.query(
                        "MATCH (p:$id) RETURN p",
                        {"id": u_id},
                    ).result_set[0]
                    v: Node = g.query(
                        "MATCH (p:$id) RETURN p",
                        {"id": v_id},
                    ).result_set[0]
                    g.add_edge(Edge(u, self.name + d, v))


@dataclass
class Station:
    """站点"""

    id: int
    zh: str
    en: str

    def save(self, g: Graph):
        """Save self to the database."""
        g.add_node(Node(label=self.id, properties={"zh": self.zh, "en": self.en}))
