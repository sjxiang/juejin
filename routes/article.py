from flask import (
    Blueprint, request
)
from sqlalchemy import exc

from utils.log import logger
from utils.serializer import HttpCode, success, error

from models.article import Article 
from models.user import User

import json

# 全局变量
from utils.consts import user_id as admin


main = Blueprint('article', __name__)


# 添加文章
@main.route("/new", methods=['POST'])
def new_article():

    logger.info('访问 new_article 页面')
    
    data = json.loads(request.data)
    
    title = data.get("title")
    content = data.get("content")
    tag = data.get("tag")
    topic = data.get("topic")    
    user_id = admin  # 全局变量
        
    try:
        item = Article.add_article(title=title, content=content, tag=tag, user_id=user_id, topic=topic)    
        return success(msg="添加文章成功", data=item)    
    except exc.SQLAlchemyError as e:
        logger.error('add_article error, {}'.format(e))
        return error(code=HttpCode.db_error, msg="添加文章失败")
        
    

# 发表文章
@main.route("/publish", methods=['GET'])
def publish_article():
    
    logger.info('访问 publish_article 页面')
    
    article_id = request.args.get("_id")
    
    try:
        item = Article.query_article_by_id(1, article_id=article_id)
        if item is None:
            return error(code=HttpCode.params_error, msg="文章不存在")
    
        Article.mod_drafted(article_id)
        return success(msg="发表文章成功")
    except exc.SQLAlchemyError as e:
        logger.error('mod_drafted error, {}'.format(e))
        return error(code=HttpCode.db_error, msg="发表文章失败")



# 搜素文章
# 127.0.0.1:9000/article/search?page_num=1&keyword=vue
@main.route("/search", methods=['GET'])
def search_article():

    logger.info('访问 search_article 页面')

    page_num = request.args.get("page_num")
    keyword = request.args.get("keyword")

    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)  

    # 因为掘金主基调是前端
    if keyword is None:
        keyword = 'fe'    
        
    try:
        total_count, total_pages, items = Article.query_article_by_field(page_num, keyword=keyword)
        return success(msg="success", data={'total_count': total_count, 'total_pages': total_pages, 'items': items})
    except exc.SQLAlchemyError as e:
        logger.error('search_article error, {}'.format(e))
        return error(code=HttpCode.db_error, msg="搜素文章失败")
    

# 点击最新文章
# 127.0.0.1:9000/article/latest?page_num=1&topic=fe
@main.route("/latest", methods=['GET'])
def latest():
    
    logger.info('访问 latest 页面')

    page_num = request.args.get("page_num")
    topic = request.args.get("topic")

    if page_num is None or int(page_num) < 1:
        page_num = 1
        
    if topic is None:
        topic = 'fe'
            
    try:     
        total_count, total_pages, items = Article.query_latest_article_by_page(page_num, topic)
        return success(
            msg="success", data={'total_count': total_count, 'total_pages': total_pages, 'items': items})

    except exc.SQLAlchemyError as e:
        logger.error('query_latest_article_by_page error, {}'.format(e))
        return error(code=HttpCode.db_error, msg="查询最新文章失败")
    

# 点击推荐文章
# 127.0.0.1:9000/article/recommend?page_num=1&topic=fe
@main.route("/recommend", methods=['GET'])
def recommend():
    
    logger.info('访问 recommend 页面')
    
    page_num = request.args.get("page_num")
    topic = request.args.get("topic")

    if page_num is None or int(page_num) < 1:
        page_num = 1
        
    if topic is None:
        topic = 'fe'
            
    try:     
        total_count, total_pages, items = Article.query_recommend_article_by_page(page_num, topic)
        return success(
            msg="success", data={'total_count': total_count, 'total_pages': total_pages, 'items': items})

    except exc.SQLAlchemyError as e:
        logger.error('query_recommend_article_by_page error, {}'.format(e))
        return error(code=HttpCode.db_error, msg="查询最新文章失败")
    

# 获取文章详情
# 127.0.0.1:9000/article/detail?_id=23
@main.route("/detail", methods=['GET'])
def detail():
    # logger.info('访问 detail 页面')

    article_id = request.args.get("_id")
    
    try:
        # 获取文章所有信息
        article = Article.query_article_by_id(article_id)
        if article is None:
            return error(code=HttpCode.params_error, msg="文章不存在")
        
        # 获取文章作者信息
        user = User.query_user_by_userid(article.user_id)
        if user is None:
            return error(code=HttpCode.params_error, msg="作者不存在")
        
        # 获取文章评论信息
        
        # 获取文章点赞信息
        
        # 获取我是否点赞了这个文章
        is_fav = 1

        return success(msg="获取文章详情成功", data={'article': article, 'user': user, 'is_fav': is_fav})
    
    except exc.SQLAlchemyError as e:
        logger.error('query_article_by_id error, {}'.format(e))
        return error(code=HttpCode.db_error, msg="查询文章详情失败")
        
    