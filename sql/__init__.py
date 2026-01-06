from config import Config
from .coinflip import Coinflip
from .user import User
from .sqlbase import SqlBase

class Sql(User, Coinflip, SqlBase):
    def __init__(self, db_url: str, config: Config):
        super().__init__(db_url, config)

__all__ = ["SqlBase", "Coinflip", "User", "Sql"]