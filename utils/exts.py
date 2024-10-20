
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

import config


# 扩展


def db_connent():
    """ 创建数据库连接 """ 
    
    # 这就是套路
    engine = create_engine(url=config.database_url, echo=True, pool_size=10, max_overflow=30)  # 是否打印 sql 语句
    session = sessionmaker(bind=engine, autoflush=False)
    db_session = scoped_session(session)  # 线程安全
    Base = declarative_base()  # ORM 基类
    
    return db_session, Base, engine

         