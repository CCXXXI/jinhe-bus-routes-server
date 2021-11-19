from dataclasses import asdict, dataclass

from redis import Redis


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

    stations: list[str] = None
    """不分上下行的沿线站点的 `id_`"""

    up_stations: list[str] = None
    """上行沿线站点的 `id_`"""

    down_stations: list[str] = None
    """下行沿线站点的 `id_`"""

    def __post_init__(self):
        """Convert bool to int as Redis doesn't support bool."""
        self.directional = int(self.directional)

    def save(self, r: Redis):
        """Save self to the database."""
        # basic
        mapping = asdict(self)
        mapping.pop("stations")
        mapping.pop("up_stations")
        mapping.pop("down_stations")
        r.hset(f"Route:{self.name}", mapping=mapping)

        # graph
