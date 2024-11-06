from sqlalchemy import Table, or_
from datetime import datetime
from models.user import User
from utils.bootstrap import db_connect


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
        record = cls(topic=topic, title=title, content=content, tag=tag, browse_num=0, user_id=user_id, is_drafted=0, is_original=0, created_at=datetime.now(), updated_at=datetime.now(), status=0)
        db_session.add(record)
        db_session.commit()
        return record.to_dict()
    
    
    @classmethod
    def batch_add_article(cls, **kwargs):
        """
        批量添加文章
        """
        pass
    
    
    @classmethod
    def query_recommend_article_by_page(cls, page_num, topic):
        """
        <推荐>, 分页查询文章, 但是不要草稿
        """
        
        # 当前第几页, 默认第1页
        page_num = 1 if page_num <= 0 else int(page_num)
        # 每页显示多少条记录
        page_size = 10
        # 总的记录数
        total_count = db_session.query(Article).count()
        # 一共有多少页
        total_pages = (total_count + page_size - 1) // page_size
        
        skip = (page_num - 1) * page_size
            
        result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(Article.topic == topic, Article.is_drafted == 1).order_by(Article.browse_num.desc()).limit(page_size).offset(skip).all()
        items = cls.build_article_list_from_rows(result)
        
        return total_count, total_pages, items
    
            
    @classmethod
    def query_latest_article_by_page(cls, page_num, topic):
        """
        <最新>, 分页查询文章, 但是不要草稿
        """
        page_num = int(page_num)
        page_size = 10
        total_count = db_session.query(Article).count()
        total_pages = (total_count + page_size - 1) // page_size
        start = (page_num - 1) * page_size

                
        result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(Article.topic == topic, Article.is_drafted == 1).order_by(Article.created_at.desc()).limit(page_size).offset(start).all()
        items = cls.build_article_list_from_rows(result)
        return total_count, total_pages, items


    @classmethod
    def query_article_by_field(cls, page_num, keyword):
        """
        根据关键词, 分页查询文章, 但是不要草稿
        """
        page_num = int(page_num)
        page_size = 10
        
        total_count = db_session.query(Article).count()
        total_pages = (total_count + page_size - 1) // page_size
        
        skip = (page_num - 1) * page_size
        
        condition_1 = or_(Article.title.like("%"+keyword+"%"), Article.content.like("%"+keyword+"%"))

        result = db_session.query(Article, User.nickname).join(User, User.id == Article.user_id).filter(condition_1, Article.is_drafted == 1).order_by(Article.browse_num.desc()).limit(page_size).offset(skip).all()
        items = cls.build_article_list_from_rows(result)
        
        return total_count, total_pages, items
    
        
    @classmethod
    def query_article_by_id(cls, article_id):
        """
        根据文章 id, 查询文章详情
        """
        result = db_session.query(Article).filter_by(id=article_id).one_or_none()
        if result is None:
            return None
        else:
            return result.to_dict()


        
    @classmethod
    def mod_browse_num(cls, article_id, num):
        """
        文章浏览量, ++
        
        UPDATE `article` SET `browse_num` = '100' WHERE `id` = 24;
        """
        result = db_session.query(Article).filter_by(id=article_id).one_or_none()
        result.browse_num = num
        db_session.commit()
        
    
    
    @classmethod
    def mod_drafted(cls, article_id):
        """
        更改文章的状态, 草稿/发布
        
        UPDATE article SET is_drafted='1' WHERE article.id = 23; 
        """    
        result = db_session.query(Article).filter_by(id=article_id).one_or_none()
        result.is_drafted = 1
        db_session.commit()
        
    
    @staticmethod
    def build_article_list_from_rows(result):
        """
        1. 遍历 <class 'list'> 中的 <class'sqlalchemy.engine.row.Row'>
        2. 把 <class'sqlalchemy.engine.row.Row'> 转换成 <class'models.article.Article'>
        3. 把 <class'models.article.Article'> 转换成 <class'dict'>
        """
        ll = []
        
        for item in result:
            ll.append(item[0].to_dict())

        return ll
        
    
    def to_dict(self):
        
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
            '标签': self.tag.split(','),
            '草稿': self.is_drafted == 0,
            '原创': self.is_original == 0,
            '创建日期': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            '更新日期': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }    
        
                                                                                                                                                                                                                                                                                                                                                                     