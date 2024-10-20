
from sqlalchemy import Table, or_
from utils.exts import db_connent
from models.user import User

db_session, Base, engine = db_connent()

class Article(Base):
    __table__ = Table("article", Base.metadata, autoload_with=engine)

    def find_article(self,page,article_type="recommend",):
        #
        page = int(page)
        if page < 1:
            page = 1
            
        page_count = 10
        count=page*page_count
        # 通过用户 id 查询 fav_id 在查询 artcile_id
        if article_type == "recommend":
            result = (db_session.query(Article, User.nickname)
                      .join(User, User.user_id == Article.user_id)
                      .filter(Article.drafted == 1)
                      .order_by(Article.browse_num.desc())
                      .limit(count).all())
        else:
            result = (db_session.query(Article, User.nickname)
                      .join(User, User.user_id == Article.user_id)
                      .filter(Article.label_name == article_type, Article.drafted == 1)
                      .order_by(Article.browse_num.desc())
                      .limit(count).all())

        return result

    def search_article(self,page,keyword):
        if int(page) < 1:
            page = 1
        count = int(page) * config[env].page_count
        result = db_session.query(
            Article,User.nickname).join(
            User,User.user_id==Article.user_id).filter(
            or_(Article.title.like("%"+keyword+"%"), Article.article_content.like("%"+keyword+"%"))
        ).order_by(
            Article.browse_num.desc()
        ).limit(count).all()
        return result

