import logging
from datetime import timedelta


class Config(object):
    """ base configuration """        
    
    # 密钥 
    SECRET_KEY = "p4zBYlTGH@0NMbk5"

    # 数据库
    MySQL_USERNAME = 'root'
    MySQL_PASSWORD = 'my-secret-pw'
    MySQL_HOST = "127.0.0.1"
    MySQL_PORT = 13306
    MySQL_DATABASE = 'juejin'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
            MySQL_USERNAME, 
            MySQL_PASSWORD, 
            MySQL_HOST, 
            MySQL_PORT, 
            MySQL_DATABASE
        )
    
    # 缓存
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 0


    # 日志
    LOG_PREFIX = 'gua'
    
    # 日志文件路径
    from pathlib import Path
    base_dir = Path(__file__).resolve().parent.parent  # 上一级目录
    import os 
    LOG_FILE = os.path.join(base_dir, 'logs', 'gua.log')

    LOG_LEVEL = logging.INFO



    
# 开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    

# 测试环境
class TestingConfig(Config):
    pass
    
    
# 生产环境
class ProductionConfig(Config):
    DEBUG = False    
    LOG_LEVEL = logging.ERROR
    
    
    
config = {
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
    'pro': ProductionConfig,
}



