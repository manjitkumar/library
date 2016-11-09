from library.middleware.filter import (
    CLIENT_ACTIVITY_PREFIX,
    CLIENT_BLOCKED_PREFIX,
    CLIENT_PERMANENTLY_BLOCKED_PREFIX,
    APIRedis
)


redis_instance = APIRedis()


def unblock_client(client_indentity):
    """
    unblocks client to use CAPTCHA free APIs. 
    """
    client_block_key = CLIENT_BLOCKED_PREFIX + client_indentity
    return redis_instance.delete(client_block_key)
