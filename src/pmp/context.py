from dataclasses import dataclass
from logging import Logger

from mariadb import ConnectionPool


@dataclass
class PmpPipelineContext:
    pool: ConnectionPool
    access_token: str
    logger: Logger | None
