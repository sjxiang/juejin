from sqlalchemy import Table, exc, or_
from datetime import datetime

from utils.bootstrap import db_connect


db, Base, engine = db_connect()


class Favorite(Base):
    __table__ = Table("favorite", Base.metadata, autoload_with=engine)

    @classmethod
    def add_favorite(cls, article_id, user_id):

        """
        添加收藏
        
        查询这个用户是否收藏过, 收藏过就不添加了, 没收藏过就添加
        """
        item = db.query(Favorite).filter_by(article_id = article_id, user_id = user_id).one_or_none()
        
        
        pass
    
    