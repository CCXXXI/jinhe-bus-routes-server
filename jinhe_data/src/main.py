import logging
from subprocess import run
from time import sleep

from redis import Redis
from redis.exceptions import ConnectionError
from redisgraph import Graph
from tqdm import tqdm

from .data import routes, stations

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

r = Redis(decode_responses=True)
g = Graph("g", r)


def save():
    """Save all data to the database."""
    # to resolve magic ConnectionError
    while True:
        try:
            logging.info(f"{r.ping()=}")
        except ConnectionError as e:
            logging.warning(e)
        else:
            break
        sleep(1)

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
