from dataclasses import asdict, dataclass
from itertools import pairwise

from redis import Redis
from redisgraph import Edge, Graph, Node


@dataclass
class Route:
    """路线"""

    directional: int
    """无向为false，不仅仅是环线，还有G62路等单向线路"""

    interval: int
    """班次间隔（分钟）"""

    kilometer: float
    """单向里程（公里）"""

    name: str
    """线路名"""

    onewayTime: str
    """运行时⻓"""

    route: str
    """线路走向"""

    runtime: str
    """运营时间，和班次表有略微不一致"""

    type: str
    """线路类型"""

    stations: list[int] = None
    """不分上下行的沿线站点的 `id`"""

    up_stations: list[int] = None
    """上行沿线站点的 `id`"""

    down_stations: list[int] = None
    """下行沿线站点的 `id`"""

    def __post_init__(self):
        """Convert bool to int as Redis doesn't support bool."""
        self.directional = int(self.directional)

    def save(self, r: Redis, g: Graph):
        """Save self to the database."""
        # basic
        mapping = asdict(self)
        for key in ("name", "stations", "up_stations", "down_stations"):
            del mapping[key]
        r.hset(f"Route:{self.name}", mapping=mapping)

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
        g.add_node(Node(label=self.id, properties={"zh": self.zh, "en": self.en}))
