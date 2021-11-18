import logging

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://a7ad189559a44dd8819c0862367ecbfe@o996799.ingest.sentry.io/6042882",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Yet another fake API."""
    return "Hello World!"


if __name__ == "__main__":
    app.run()
