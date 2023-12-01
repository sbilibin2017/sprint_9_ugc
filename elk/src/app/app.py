import logging
import os
import random

import dotenv
import logstash
import sentry_sdk
from flask import Flask, request
from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(__name__)

dotenv.load_dotenv()

sentry_dsn = os.getenv('SENTRY_DSN')

sentry_sdk.init(
    dsn=sentry_dsn,
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True

app.logger.addFilter(RequestIdFilter())
app.logger.addHandler(logstash_handler)

@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is requred')


@app.route('/')
def index():
    result = random.randint(1, 50)
    app.logger.info(f'Пользователю досталось число {result}')
    return f"Ваше число {result}!"

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0



