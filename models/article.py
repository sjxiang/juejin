
from sqlalchemy import Table, exc, or_
from sqlalchemy.orm import Session

from utils.bootstrap import db_connect
from utils.log import logger
from utils.errno import ErrNo

from models.user import User


db_session, Base, engine = db_connect()


class Article(Base):
    __table__ = Table("article", Base.metadata, autoload_with=engine)

    def __init__(self, **kwargs):
        # `label`, `title`, `content`, `tag`, `user_id`
        pass
    
    
    @classmethod
    def query_recommend_article_by_page(cls, page, label):
        """
        分页查询<推荐>文章, 但是不要草稿

        page, 页数
        page_size, 每页显示的文章数量, 默认10条
        label, 文章标签
        """
        
        page_size = 10
        start = (page - 1) * page_size

        try:        
            result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(Article.label == label, Article.drafted == 1).order_by(Article.browse_num.desc()).limit(page_size).offset(start).all()
            return {'code': ErrNo.OK.value, 'message': 'success', 'data': result}
        except exc.SQLAlchemyError as e:
            logger.error('query_latest_article_by_page error, {}'.format(e))
            return {'code': ErrNo.DATABASE_ERROR.value, 'message': 'database error'}
            
            
    @classmethod
    def query_latest_article_by_page(cls, page, label):
        """
        分页查询<最新>文章, 但是不要草稿
        """
        
        page_size = 10
        start = (page - 1) * page_size

        try:        
            result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(Article.label == label, Article.drafted == 1).order_by(Article.created_at.desc()).limit(page_size).offset(start).all()
            return {'code': ErrNo.OK.value, 'message': 'success', 'data': result}
        except exc.SQLAlchemyError as e:
            logger.error('query_recommend_article_by_page error, {}'.format(e))
            return {'code': ErrNo.DATABASE_ERROR.value, 'message': 'database error'}
        

    @classmethod
    def query_article_by_field(cls, page, keyword):

        """
        根据关键词, 分页查询文章, 但是不要草稿
        """
        page_size = 10
        start = (page - 1) * page_size
        
        condition_1 = or_(Article.title.like("%"+keyword+"%"), Article.content.like("%"+keyword+"%"))

        try:        
            result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(condition_1, Article.drafted == 1).order_by(Article.browse_num.desc()).limit(page_size).offset(start).all()
            return {'code': ErrNo.OK.value, 'message': 'success', 'data': result}
        except exc.SQLAlchemyError as e:
            logger.error('query_article_by_field error, {}'.format(e))
            return {'code': ErrNo.DATABASE_ERROR.value, 'message': 'database error'}
        

    @classmethod
    def mod_browse_num(cls, article_id, num):
        """
        文章浏览量, ++
        """
        pass
    
    
    @classmethod
    def mod_drafted(cls, article_id):
        """
        更改文章的状态, 草稿/发布
        """
        try:
            pass
        except exc.SQLAlchemyError as e:
            logger.error('mod_drafted error, {}'.format(e))
            return {'code': ErrNo.DATABASE_ERROR.value,'message': 'database error'}
    

    def to_dict(self):
        
        is_drafted = False
        
        if self.drafted == 1:
            is_drafted = True

    
        is_original = True
        
        if self.type == 1:
            is_original = False
        
        
        return {
            'id': self.id,
            '分类标签': self.label,
            '标题': self.title,
            '内容': self.content,
            '浏览量': self.browse_num,
            '草稿': is_drafted,
            '原创': is_original,
            '创建日期': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            '更新日期': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }    
        