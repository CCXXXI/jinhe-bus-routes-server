import logging
from subprocess import run

from redis import Redis
from redisgraph import Graph
from tqdm import tqdm

from .data import routes, stations

r = Redis(decode_responses=True)
g = Graph("g", r)


def save():
    """Save all data to the database."""
    # meta
    version = run(
        ["git", "rev-parse", "HEAD"], capture_output=True, check=True
    ).stdout.strip()
    logging.info(f"{version=}")
    r.set("version", version)

    # normal
    for station in tqdm(stations, "stations"):
        station.save(g)
    g.commit()
    for route in tqdm(routes, "routes"):
        route.save(r, g)

    # persistence
    r.save()


if __name__ == "__main__":  # pragma: no cover
    save()
