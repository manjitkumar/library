import redis

from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured

from captcha.models import Captcha
from captcha.serializers import CaptchaSerializer


CLIENT_ACTIVITY_PREFIX = 'client_activity:'
CLIENT_BLOCKED_PREFIX = 'client_blocked:'
CLIENT_PERMANENTLY_BLOCKED_PREFIX = 'client_premanently_blocked:'


try:
    DOSFILTERING_CONFIG = settings.DOSFILTERING_CONFIG
    REDIS_CONFIG = DOSFILTERING_CONFIG['REDIS']
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
        client_indentity = self.get_identity(request)

        # attach client_identity to request object.
        request.client_indentity = client_indentity
        print request.path
        if (
            self.is_blocked(client_indentity) and
            'validate_captcha' not in request.path   # ignore captcha validation requests.
        ):
            return JsonResponse(
                self.get_captcha(),
                content_type="application/json"
            )
        else:
            self.update_client_activity(client_indentity)

    def get_identity(self, request):
        """
        Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
        if present and number of proxies is > 0. If not use all of
        HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.

        source : https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/throttling.py#L26
        """
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')
        num_proxies = settings.NUM_PROXIES

        if num_proxies is not None:
            if num_proxies == 0 or xff is None:
                return remote_addr
            addrs = xff.split(',')
            client_addr = addrs[-min(num_proxies, len(addrs))]
            return client_addr.strip()

        return ''.join(xff.split()) if xff else remote_addr

    def is_blocked(self, client_indentity):
        """
        returns True if given client_indentity is_blocked otherwise False.
        """
        client_blocked_key = CLIENT_BLOCKED_PREFIX + client_indentity
        return self.redis_instance.exists(client_blocked_key)

    def update_client_activity(self, client_indentity):
        """
        updates the client request activity.
        """
        activity_key = CLIENT_ACTIVITY_PREFIX + client_indentity
        client_request_count = self.redis_instance.get(activity_key)
        if client_request_count is None:
            client_request_count = 1
            self.redis_instance.set(
                activity_key,
                client_request_count,
                DOSFILTERING_CONFIG['ACTIVITY_TIMEFRAME']
            )
        else:
            client_request_count = int(client_request_count)

            if client_request_count > DOSFILTERING_CONFIG['ALLOWED_REQ_PER_MIN']:
                self.block_client(client_indentity)
            else:
                # increment request count by 1 for every request against given client_id.
                self.redis_instance.incr(activity_key)

    def block_client(self, client_indentity, permanently=False):
        """
        blocks the given client_indentity.
        permanently flag determines whether the given client_indentity should be
        blocked permanently or temporarily.
        """
        client_block_key = CLIENT_BLOCKED_PREFIX + client_indentity
        self.redis_instance.set(
            client_block_key,
            '',
            None if permanently else DOSFILTERING_CONFIG['BLOCKAGE_TTL'],
        )

    def get_captcha(self):
        """
        returns a random captcha object from Captcha model.
        """
        captcha = Captcha.objects.filter().first()
        serializer = CaptchaSerializer(captcha)
        return serializer.data
