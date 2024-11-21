from time import sleep
from mariadb import PoolError, mariadb


def wait_for_pool_connection(pool: mariadb.ConnectionPool) -> mariadb.Connection:
    """Blocks the current thread until a connection is available in the given connection pool, then returns it."""
    while True:
        try:
            return pool.get_connection()
        except PoolError:
            sleep(0.1)
            continue
