from sqlalchemy import Table, exc, or_
from sqlalchemy.orm import Session

from utils.bootstrap import db_connect
from utils.log import logger
from utils.errno import ErrNo
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
        try:
            db_session.add(cls(**kwargs))
            db_session.commit()
            return {'code': 0}
        except exc.SQLAlchemyError as e:
            logger.error(f'new user error, {e}')
            return {'code': 1}        

    
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
        try:
            db_session.query(User).filter_by(id=user_id).delete()
            db_session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(f'delete user error, {e}')
            return {'code': ErrNo.DATABASE_ERROR.value,'message': 'database error'}

    
    @classmethod
    def add_user(cls, email, password):
        try:
            db_session.add(cls(email=email, password=password))
            db_session.commit()
            return {'code': ErrNo.OK.value,'message':'success'}    
        except exc.SQLAlchemyError as e:
            logger.error(f'add_user error, {e}')
            return {'code': ErrNo.DATABASE_ERROR.value,'message': 'database error'}
    
       
    @classmethod
    def mod_user(cls, user_id):
        pass
    
    
    @classmethod
    def query_user_by_userid(cls, user_id):      
        try:
            result = db_session.query(User).filter_by(id=user_id).one_or_none()
            
            if result is not None:
                return {'code': ErrNo.OK.value,'message':'success', 'data': result}
            else:
                return {'code': ErrNo.DATABASE_RECORD_NOT_FOUND.value,'message': 'record not exists'}
        except exc.SQLAlchemyError as e:
            logger.error(f'query_user_by_userid error, {e}')
            return {'code': ErrNo.DATABASE_ERROR.value,'message': 'database error'}

        
    @classmethod
    def query_user_by_field(cls):
        pass
    
    
    @classmethod
    def query_user_by_email(cls, email):
        """
        通过邮箱, 查找用户
        SELECT * FROM `user` WHERE email = ?;
        """   
        try:
            record = db_session.query(User).filter_by(email=email).one_or_none()
            return {'code': 0, 'data': record}
        except exc.SQLAlchemyError as e:
            logger.error('query_user_by_email error {}, email, {}'.format(e, email))
            return {'code': 1, 'message': 'database error'}
    
    
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
            
        if result is not None:
            try:
                result.password = new_password
                db_session.commit()
                return {'code': ErrNo.OK.value,'message':'success'}
            except exc.SQLAlchemyError as e:
                logger.error('mod_password error, {}'.format(e))
                return {'code': ErrNo.DATABASE_ERROR.value,'message': 'database error'}
        else:
            return {'code': ErrNo.DATABASE_RECORD_NOT_FOUND.value, 'message': 'record not exists'}
        
        
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
    
    
        