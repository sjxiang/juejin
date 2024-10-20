
from sqlalchemy import Table
from utils.exts import db_connent
from utils.utils import hashed_password


db_session, Base, engine = db_connent()

class User(Base):
    # 表结构的反射加载
    __table__ = Table("user_info", Base.metadata, autoload_with=engine)
    
    def find_one(self, input_id):
        return db_session.query(User).filter_by(id=input_id).first()

    @classmethod
    def find_one_by_email(cls, input_email):
        
        """
        通过邮箱, 查找用户
        
        SELECT 
            id, nickname, password, email, signature, avatar_url, sex, role_id, is_admin, is_streamer, is_active, last_message_read_at, created_at, updated_at, deleted_at
        FROM 
            user_info
        WHERE 
            email = 'tyr@cisco.cn'
        LIMIT 
            1;
        
        """
        return db_session.query(User).filter_by(email=input_email).first()

    def find_all(self):
        pass

    def update(self, **kwargs):
        """
        更新用户信息
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        db_session.commit()


    @classmethod
    def delete(cls, input_user_id):
        """
        软删除
        """
        db_session.query(User).filter_by(id=input_user_id).delete()

    
    @classmethod
    def create(cls, **kwargs):

        """
        注册一个新用户
        
        INSERT INTO user_info 
            (nickname, password, email, deleted_at)
        VALUES 
            ('tyr', ''e10adc3949ba59abbe56e057f20f883e', 'tyr@cisco.com', NULL);

        """
        user = User(**kwargs)
        db_session.add(user)
        db_session.commit()
        return user


    def reset_password(self, user_id, new_password):
        """
        重置用户密码
        """
        row = db_session.query(User).filter_by(id=user_id).first()
        row.password = hashed_password(new_password)       
        db_session.commit()
    
    
    





