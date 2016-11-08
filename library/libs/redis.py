import redis

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# get an redis instance
REDIS_CONFIG = settings.REDIS_CONFIG


class APIRedis(object):
    '''
    APIRedis class is to make connections with redis server and
    keep the redis operations as re-usuable methods.
    '''

    _instances = {
        'SESSION_DB': None,
        'DOS_IP_FILTER_DB': None,
    }

    def __new__(cls, *args, **kwargs):
        ''' Create singleton instance per redis database'''
        database = kwargs.get('db')
        host = kwargs.get('host')
        port = kwargs.get('port')
        # Check whether we already have an instance for cached db
        if database and database in cls._instances:
            if cls._instances[database] is None:
                try:
                    # Create and remember instance
                    cls._instances[database] = redis.StrictRedis(
                        host=host,
                        port=port,
                        db=REDIS_CONFIG[database]
                    )
                except KeyError as inst:
                    raise ImproperlyConfigured(
                        'Redis database is not configured\
                        in settings.REDIS_CONFIG'
                    )

            return cls._instances[database]
        else:
            raise ImproperlyConfigured(
                'Redis database is not configured in cls._instances'
            )
