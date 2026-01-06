from typing import Any, Optional
from sqlalchemy import DateTime, create_engine, Column, BigInteger, String, Boolean, Integer, JSON, or_
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Literal, List, Callable, Any
from datetime import datetime, timedelta
import shortuuid
from functools import wraps
import random
import inspect

from utils import Status
from config import Config

class SqlBase:
    Base = declarative_base()

    def __init__(self, db_url: str, config: Config) -> None:
        self.config = config
        self.engine: Engine = create_engine(
            db_url,
            echo=False,
            future=True,
        )

        self.SessionLocal: sessionmaker[Session] = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            future=True,
        )

    def create_tables(self) -> None:
        self.Base.metadata.create_all(self.engine)

    def session(self) -> Session:
        return self.SessionLocal()