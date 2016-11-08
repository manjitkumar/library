import redis

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


try:
    REDIS_CONFIG = settings.DOSFILTERING_CONFIG['REDIS']
except AttributeError as inst:
    raise ImproperlyConfigured(inst.message)


class APIRedis(object):
    """
    APIRedis class is to make connections with redis server and
    keep the redis operations as re-usuable methods.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        ''' Create singleton instance '''
        # Check whether we already have an instance
        if cls._instance is None:
            try:
                # Create and remember instance
                cls._instance = redis.StrictRedis(
                    host=REDIS_CONFIG['HOST'],
                    port=REDIS_CONFIG['PORT'],
                    db=REDIS_CONFIG['DB'],
                )
            except KeyError as inst:
                raise ImproperlyConfigured(
                    'Redis settings are not properly configured '
                    'in settings.REDIS_CONFIG. Please verify with '
                    'setup/installation docs.'
                )

        return cls._instance


class DoSFilterMiddleware(object):
    """
    This class acts as a django middleware to intercept every request
    in order to make sure that nobody is hitting this application with 
    a DoS attack.
    """
    redis_instance = APIRedis()

    def process_request(self, request):
        """
        process_request() is called on each request, before Django 
        decides which view to execute. for more details on process_request @ 
        https://docs.djangoproject.com/en/1.8/topics/http/middleware/#process_request
        """

        client_ip_address = self.get_identity(request)

        if self.is_blocked(client_ip_address):
            pass
        else:
            pass


    def get_identity(self, request):
        """
        Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
        if present and number of proxies is > 0. If not use all of
        HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.

        """
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')
        return xff.split(',')[0].strip() if xff else remote_addr

    def is_blocked(self, ip_address):
        """
        returns True if given ip_address is is_blocked otherwise False.
        """
        return self.redis_instance.exists(ip_address)

