from sqlalchemy import Table

from utils.bootstrap import db_connect

db_session, Base, engine = db_connect()


class User(Base):
    # 表结构的反射加载
    __table__ = Table("user", Base.metadata, autoload_with=engine)
    
    @classmethod
    def new(cls, **kwargs):
        """
        创建一个新用户
        """
        db_session.add(cls(**kwargs))
        db_session.commit()

    
    @classmethod
    def find_one(cls, user_id):
        pass


    @classmethod
    def find_by(cls, field, value):
        pass
    
    
    def find_all(cls):
        pass

    
    @classmethod
    def delete(cls, user_id):
        """
        删除用户
        """
        db_session.query(User).filter_by(id=user_id).delete()
        db_session.commit()
    
    
    @classmethod
    def add_user(cls, email, password):
        db_session.add(cls(email=email, password=password))
        db_session.commit()
        
       
    @classmethod
    def mod_user(cls, user_id):
        pass
    
    
    @classmethod
    def query_user_by_userid(cls, user_id):      
        
        result = db_session.query(User).filter_by(id=user_id).one_or_none()
            
        if result is not None:
            return result.to_dict()
        else:
            return None

        
    @classmethod
    def query_user_by_field(cls):
        pass
    
    
    @classmethod
    def query_user_by_email(cls, email):
        """
        通过邮箱, 查找用户
        SELECT * FROM `user` WHERE email = ?;
        """   
        result = db_session.query(User).filter_by(email=email).one_or_none()

        if result is not None:
            return result.to_dict()
        else:
            return None
    
    
    @classmethod
    def query_user_all(cls):
        pass
    
    
    @classmethod
    def query_user_by_page(cls):
        pass
    

    @classmethod
    def mod_password(cls, user_id, new_password):
        """
        修改密码
        """
        result = db_session.query(User).filter_by(id = user_id).one_or_none()
        result.password = new_password
        db_session.commit()
                
        
    def to_dict(self):
        
        return {
            'id': self.id,
            '昵称': self.nickname,
            '邮箱': self.email,
            '密码': '******',
            '自我介绍': self.about_me,
            '头像': self.avatar,
            '创建时间': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            '更新时间': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            '删除时间': self.deleted_at.strftime('%Y-%m-%d %H:%M:%S') if self.deleted_at is not None else None,
        }    
    
    
        