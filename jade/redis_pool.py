import django_redis.pool


class ConnectionFactory(django_redis.pool.ConnectionFactory):
    """
    Custom ConnectionFactory that injects the decode_responses parameter.
    """

    def get_connection(self, params):
        params["decode_responses"] = True
        return super(ConnectionFactory, self).get_connection(params)