from redis import Redis
from redisgraph import Graph
from tqdm import tqdm

from data import routes, stations


def save():
    """Save all data to the database."""
    r = Redis()
    g = Graph("g", r)

    for station in tqdm(stations, "stations"):
        station.save(g)
    for route in tqdm(routes, "routes"):
        route.save(r, g)

    g.commit()
    r.save()


if __name__ == "__main__":
    save()
