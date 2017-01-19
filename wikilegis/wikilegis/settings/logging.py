from .application import DEBUG
from decouple import config
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s (%(name)s) %(levelname)s: %(message)s'
            }
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'interval': 24,
                'backupCount': 7,
                'encoding': 'UTF-8',
                'formatter': 'verbose',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': config('LOG_DIR',
                                   default=BASE_DIR + '/wikilegis.log'),
            }
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
            },
        },
    }
