from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import redis

from utils.config import config
from utils.consts import env

"""
初始化 db 连接
"""

def db_connect():
    
    cfg = config[env]
    
    sqlalchemy_database_uri = cfg.SQLALCHEMY_DATABASE_URI
    
    """ 这就是套路, 连接数据库 """ 

    engine = create_engine(url=sqlalchemy_database_uri, echo=cfg.DEBUG, pool_size=5)  
    # 创建 db session 对象
    session = sessionmaker(bind=engine, autoflush=False)
    # 确保线程安全
    db_session = scoped_session(session)  
    
    # ORM 基类
    Base = declarative_base()
    
    return db_session, Base, engine


def redis_connect():
    
    """ 连接 redis """
    
    cfg = config[env]

    redis_host = cfg.REDIS_HOST
    redis_port = cfg.REDIS_PORT
    redis_db = cfg.REDIS_DB

    pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
    
    return redis.Redis(connection_pool=pool)