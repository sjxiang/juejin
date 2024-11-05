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
    
    if response.get('code') == 0:
        record = response.get('data')
        logger.info("查找用户成功, {}".format(record.to_dict()))
    elif response.get('code') == 20001:
        logger.info("查找用户失败, {}".format(response['message']))
    else:
        logger.info("查找用户失败, {}".format(response['message']))


def test_find_latest_article():
    response = Article.query_latest_article_by_page(1, 'fe')
    
    if response['code'] == 0:
        data = response.get('data')
        
        for item in data:
            logger.info("文章, {}".format(item[0].to_dict()))
            
        logger.info("查找最新文章列表, 成功")
        
    else:
        logger.info("查找最新文章列表, {}".format(response['message']))


def test_find_recommend_article():
    response = Article.query_recommend_article_by_page(1, 'fe')

    if response['code'] == 0:
        data = response.get('data')

        for item in data:
            logger.info("文章, {}".format(item[0].to_dict()))

        logger.info("查找推荐文章列表, 成功")

    else:
        logger.info("查找推荐文章列表, 失败 {}".format(response['message']))
        
        
def test_add_article():
    data = [
        {
            'topic': 'fe', 
            'title': 'vue 101', 
            'content': 'more...', 
            'tag': 'frontend, interview', 
            'user_id': 2333,
        },
        {
            'topic': 'fe', 
            'title': 'react framework', 
            'content': 'more...', 
            'tag': 'frontend, interview', 
            'user_id': 2333
        },
        {
            'topic': 'fe', 
            'title': 'jquery', 
            'content': 'more...', 
            'tag': 'frontend, interview', 
            'user_id': 2333
        },
        {
            'topic': 'be', 
            'title': 'gin', 
            'content': 'more...', 
            'tag': 'backend, interview', 
            'user_id': 2333
        },
        {
            'topic': 'be', 
            'title': 'kratos', 
            'content': 'more...', 
            'tag': 'backend, interview', 
            'user_id': 2333
        },
    ]
    
    for item in data:
        
        response = Article.add_article(**item)

        if response['code'] == 0:
            logger.info("添加文章, 成功")
        else:
            logger.info("添加文章, 失败, {}", response['message'])

    logger.info("添加文章, 结束")


def test_mod_drafted():
    article_id = 24

    response = Article.mod_drafted(article_id)
    
    if response.get('code') == 0:
        logger.info("修改文章状态, 成功")
    else:
        logger.info("修改文章状态, 失败, {}", response['message'])
        


def test_script():
    # test_insert_user()
    # test_find_user()
    # test_find_latest_article()
    test_find_recommend_article()
    # test_add_article()
    # test_mod_drafted()


if __name__ == '__main__':
    test_script()    
