
from sqlalchemy import Table, exc, or_
from sqlalchemy.orm import Session
from datetime import datetime

from utils.bootstrap import db_connect
from utils.log import logger
from utils.errno import ErrNo

from models.user import User


db_session, Base, engine = db_connect()


class Article(Base):
    __table__ = Table("article", Base.metadata, autoload_with=engine)

    
    @classmethod
    def add_article(cls, topic, title, content, tag, user_id):
        """
        添加文章
        
        INSERT INTO article 
            (topic, title, content, tag, user_id, browse_num, is_drafted, is_original, created_at, updated_at, status) 
        VALUES 
            ('fe', 'vue', 'more...', 'fe,interview', 2333, 0, 0, 0, '2023-05-24 15:23:54', '2023-05-24 15:23:54', 0);
        
        """
        try:
            db_session.add(cls(topic=topic, title=title, 
                    content=content, tag=tag, browse_num=0,
                    user_id=user_id, is_drafted=0, is_original=0, 
                    created_at=datetime.now(), updated_at=datetime.now(), status=0,
                ))

            db_session.commit()
            return {'code': ErrNo.OK.value,'message':'success'}    
        except exc.SQLAlchemyError as e:
            logger.error(f'add_article error, {e}')
            return {'code': ErrNo.DATABASE_ERROR.value,'message': 'database error'}
        
    
    @classmethod
    def query_recommend_article_by_page(cls, page, topic):
        """
        分页查询<推荐>文章, 但是不要草稿

        page, 页数
        page_size, 每页显示的文章数量, 默认10条
        topic, 话题
        """
        
        page_size = 10
        start = (page - 1) * page_size

        try:        
            result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(Article.topic == topic, Article.is_drafted == 1).order_by(Article.browse_num.desc()).limit(page_size).offset(start).all()
            return {'code': ErrNo.OK.value, 'message': 'success', 'data': result}
        except exc.SQLAlchemyError as e:
            logger.error('query_latest_article_by_page error, {}'.format(e))
            return {'code': ErrNo.DATABASE_ERROR.value, 'message': 'database error'}
            
            
    @classmethod
    def query_latest_article_by_page(cls, page, topic):
        """
        分页查询<最新>文章, 但是不要草稿
        """
        
        page_size = 10
        start = (page - 1) * page_size

        try:        
            result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(Article.topic == topic, Article.is_drafted == 1).order_by(Article.created_at.desc()).limit(page_size).offset(start).all()
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
            result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(condition_1, Article.is_drafted == 1).order_by(Article.browse_num.desc()).limit(page_size).offset(start).all()
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
        
        UPDATE article SET is_drafted='1' WHERE article.id = 23; 
        """    
        result = db_session.query(Article).filter_by(id=article_id).one_or_none()

        if result is not None:
            try:
                result.is_drafted = 1
                db_session.commit()
                return {'code': ErrNo.OK.value, 'message': 'success'}
            except exc.SQLAlchemyError as e:
                logger.error('mod_drafted error, {}'.format(e))
                return {'code': ErrNo.DATABASE_ERROR.value, 'message': 'database error'}
        else:
            logger.error('article is not exists')
            return {'code': ErrNo.DATABASE_RECORD_NOT_FOUND.value,'message':'record not exists'}


    def to_dict(self):
        
        # 默认是草稿
        is_drafted = True
        
        if self.is_drafted == 1:
            is_drafted = False

        # 默认是原创
        is_original = True
        
        if self.is_original == 1:
            is_original = False
        
        topics = {
            'fe': '前端',
            'be': '后端',
            'test': '测试',
            'ai': '人工智能',
            'rag': '大模型',
        }
        
        return {
            'id': self.id,
            '话题': topics[self.topic],
            '标题': self.title,
            '内容': self.content,
            '浏览量': self.browse_num,
            '草稿': is_drafted,
            '原创': is_original,
            '创建日期': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            '更新日期': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }    
        
        