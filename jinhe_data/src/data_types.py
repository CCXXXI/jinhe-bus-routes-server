from dataclasses import asdict, dataclass

from redis import Redis


@dataclass
class Line:
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

    # stations: list[str]
    # """沿线站点的 `id_`"""

    def __post_init__(self):
        """Convert bool to int as Redis doesn't support bool."""
        self.directional = int(self.directional)

    def save(self, r: Redis):
        """Save self to the database."""
        # 基础信息
        mapping = asdict(self)
        mapping.pop("stations")
        r.hset(self.name, mapping=mapping)
