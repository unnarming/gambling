from .sqlbase import SqlBase
from .structs import CoinflipStats, MinesStats
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, JSON
from utils import Status

import functools
import inspect
from typing import Literal, List, Any, Callable, Union
from utils import Check

def _make_wrapper(func: Callable, param_names: list[str]) -> Callable:
    if "discord_id" not in param_names:
        param_names.insert(0, "discord_id")

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(self, *args, **kwargs)
        bound_args.apply_defaults()

        user_ids: list[int] = []
        for name in param_names:
            if name in bound_args.arguments and bound_args.arguments[name] is not None:
                user_ids.append(int(bound_args.arguments[name]))

        for user_id in user_ids:
            if not User.get_user(self, user_id).status:
                User.create_user(self, user_id)
        return func(self, *args, **kwargs)
    return wrapper

def usercheck(*args):
    if len(args) == 1 and callable(args[0]):
        return _make_wrapper(args[0], [])
    
    param_names = list(args)
    def decorator(func: Callable):
        return _make_wrapper(func, param_names)
    return decorator

class User(SqlBase):
    class UserData(SqlBase.Base):
        __tablename__ = "users"

        discord_id: int = Column(BigInteger, primary_key=True, unique=True, index=True, nullable=False)
        balance: int = Column(BigInteger, nullable=False, default=1000)
        busy: bool = Column(Boolean, nullable=False, default=False)
        cf_stats: CoinflipStats = Column(JSON, nullable=False, default=CoinflipStats().to_dict())
        mines_stats: MinesStats = Column(JSON, nullable=False, default=MinesStats().to_dict())

    def create_user(self, discord_id: int) -> Status:
        with self.session() as session:
            user = User.UserData(discord_id=discord_id)
            session.add(user)
            session.commit()
            return Status(status=True, body=user.discord_id)

    def get_user(self, discord_id: int) -> Status:
        with self.session() as session:
            user = session.query(User.UserData).filter_by(discord_id=discord_id).first()
            if user:
                return Status(status=True, body=user)
            return Status(message="User not found")
        

    @usercheck
    def get_stats(self, discord_id: int, stats_type: Union[CoinflipStats, MinesStats]) -> CoinflipStats | MinesStats:
        with self.session() as session:
            user = session.query(User.UserData).filter_by(discord_id=discord_id).first()
            return stats_type.from_dict(getattr(user, stats_type.NAME))

    @usercheck
    def set_stats(self, discord_id: int, stats_type: Union[CoinflipStats, MinesStats], stats: CoinflipStats | MinesStats):
        with self.session() as session:
            user = session.query(User.UserData).filter_by(discord_id=discord_id).first()
            setattr(user, stats_type.NAME, stats.to_dict())
            session.commit()

    @usercheck
    def modify_balance(self, discord_id: int, amount: int) -> Status:
        with self.session() as session:
            user: User.UserData = session.query(User.UserData).filter_by(discord_id=discord_id).first()

            if user.balance + amount >= 0:
                user.balance += amount
                session.commit()
                return Status(status=True)
            else:
                user.balance = 0
                session.commit()
                return Status(status=True)

    @usercheck
    def set_balance(self, discord_id: int, amount: int) -> Status:
        with self.session() as session:
            user: User.UserData = session.query(User.UserData).filter_by(discord_id=discord_id).first()
            if amount >= 0:
                user.balance = amount
                session.commit()
                return Status(status=True)
            else:
                return Status(message="Balance would be negative")

    @usercheck
    def get_balance(self, discord_id: int) -> int:
        with self.session() as session:
            user: User.UserData = session.query(User.UserData).filter_by(discord_id=discord_id).first()
            return user.balance

    @usercheck
    def check_balance(self, discord_id: int, amount: int, user_type: Literal["self", "other"] = "self") -> Status:
        with self.session() as session:
            user: User.UserData = session.query(User.UserData).filter_by(discord_id=discord_id).first()
            if user.balance >= amount and user.balance > 0:
                return Status(status=True)
            else:
                if user_type == "self":
                    return Check.USER_BAL_SELF.to_status()
                else:
                    return Check.USER_BAL_OTHER.to_status()

    def get_highest_balances(self, num: int) -> List["User.UserData"]:
        with self.session() as session:
            return (
                session.query(User.UserData)
                .order_by(User.UserData.balance.desc())
                .limit(num)
                .all()
            )

User.usercheck = staticmethod(usercheck)
User._make_wrapper = staticmethod(_make_wrapper)