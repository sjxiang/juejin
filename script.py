from models.user import User
from models.article import Article
from utils.log import logger
from utils.common import hashed_password


def test_insert_user():
    email = 'gua@vip.cn'
    password = '123456'
    
    data = {
        'nickname': email.split("@")[0],  
        'password': hashed_password(password),
        'email': email
    }
    
    response = User.new(**data)

    if response['code'] == 0:
        logger.info("注册成功, message, {}".format(response['message']))
    else:
        logger.info("注册失败, {}".format(response['message']))
        

def test_find_user():
    email = 'gua@vip.cn'
    
    response = User.query_user_by_email(email)
    
    data = response.get('data')
    code = response['code']
    msg = response['message']
    
    if code == 0:
        logger.info("查找用户成功, {}".format(data.to_dict()))
    elif code == 20001:
        logger.info("查找用户失败, {}".format(msg))
    else:
        logger.info("查找用户失败, {}".format(msg))


def test_find_latest_article():
    response = Article.query_latest_article_by_page(1, 'fe')
    
    if response['code'] == 0:
        data = response.get('data')
        
        for item in data:
            logger.info("文章, {}".format(item[0].to_dict()))
            
        logger.info("查找最新文章列表, 成功")
        
    else:
        logger.info("查找最新文章列表, {}".format(response['message']))

def test_script():
    # test_insert_user()
    # test_find_user()
    test_find_latest_article()


if __name__ == '__main__':
    test_script()    

