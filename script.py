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
    
    User.new(**data)

    logger.info("用户注册成功")
        

from utils.common import validate_password


def test_validate_password():
    """
    测试 validate_password 函数
    """
    assert validate_password("Abc@12345") == True, "密码符合要求"
    print("测试通过")
        

def test_find_user():
    email = 'gua@vip.cn'
    
    item = User.query_user_by_email(email)
    
    if item is None:
        logger.info("查找用户, 失败")
        return
    else:
        logger.info("查找用户, 成功\n{}".format(item))
        

def test_find_latest_article():
    total_count, total_pages, items = Article.query_latest_article_by_page(1, 'fe')
    logger.info("查找最新文章列表, {}, {}, {}".format(total_count, total_pages, items))


def test_find_recommend_article():
    item = Article.query_recommend_article_by_page(1, 'fe')

    if item is None:
        logger.info("查找推荐文章列表, 失败")
        return
    else:
        logger.info("查找推荐文章列表, 成功\n{}".format(item))
        
        
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
        Article.add_article(**item)

    logger.info("添加文章, 结束")


def test_mod_drafted():
    article_id = 24

    Article.mod_drafted(article_id)
    
    logger.info("修改文章状态, 成功")
    

def test_script():
    # test_insert_user()
    # test_find_user()
    # test_find_latest_article()
    # test_find_recommend_article()
    # test_add_article()
    # test_mod_drafted()
    
    test_validate_password()


if __name__ == '__main__':
    from utils.bootstrap import redis_connect

    rds = redis_connect()
    rds.set("name", "gua")
    
    