from redis import Redis
from redisgraph import Graph
from tqdm import tqdm

from data import routes, stations

r = Redis()
g = Graph("g", r)


def save():
    """Save all data to the database."""
    for station in tqdm(stations, "stations"):
        station.save(g)
    g.commit()
    for route in tqdm(routes, "routes"):
        route.save(r, g)
    r.save()


if __name__ == "__main__":  # pragma: no cover
    save()
