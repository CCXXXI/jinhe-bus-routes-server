from dataclasses import dataclass
from itertools import pairwise

from redis import Redis
from redisgraph import Graph, Node


@dataclass
class Station:
    """站点"""

    id: int
    zh: str
    en: str

    def save(self, g: Graph):
        """Save self to the database."""
        g.add_node(Node(properties={"id": self.id, "zh": self.zh, "en": self.en}))


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

    first_service: tuple[int, ...] = None
    """不分上下行的首班沿线站点时间 (h * 60 + m)"""

    steps: tuple[int, ...] = None
    """不分上下行的每个班次离首班的分钟数"""

    up_stations: tuple[int, ...] = None
    """上行沿线站点的 `id`"""

    first_up_service: tuple[int, ...] = None
    """上行首班沿线站点时间 (h * 60 + m)"""

    up_steps: tuple[int, ...] = None
    """上行每个班次离首班的分钟数"""

    down_stations: tuple[int, ...] = None
    """下行沿线站点的 `id`"""

    first_down_service: tuple[int, ...] = None
    """下行首班沿线站点时间 (h * 60 + m)"""

    down_steps: tuple[int, ...] = None
    """下行每个班次离首班的分钟数"""

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
            (self.up_stations, "u"),
            (self.down_stations, "d"),
        ):
            if s:
                for u, v in pairwise(s):
                    g.query(
                        "MATCH (u{id:$u}), (v{id:$v}) "
                        "CREATE (u)-[:r{name:$name,d:$d}]->(v)",
                        {"u": u, "v": v, "name": self.name, "d": d},
                    )
