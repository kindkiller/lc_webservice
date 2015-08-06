__author__ = 'zoe'

import os
import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6379'))

STREAM_REDIS_CONFIG = {
    'default': {
        'host': redis_url.hostname,
        'port': redis_url.port,
        'password': redis_url.password,
        'db': 0
    },
}


CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True