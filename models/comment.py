from sqlalchemy import Table, exc, or_
from sqlalchemy.orm import Session
from datetime import datetime

from utils.bootstrap import db_connect
from utils.log import logger
from utils.errno import ErrNo



db, Base, engine = db_connect()


class Comment(Base):
    __table__ = Table("comment", Base.metadata, autoload_with=engine)

    @classmethod
    def add_comment(cls, **kwargs):
        pass
    
    
    