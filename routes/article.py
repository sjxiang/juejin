from flask import (
    Blueprint, request, session
)
from sqlalchemy import exc

from utils.log import logger
from utils.common import random_code, send_email, random_str, validate_password, hashed_password
from utils.serializer import HttpCode, success, error

from models.article import Article 


import json


main = Blueprint('article', __name__)


# 添加文章
@main.route("/new", methods=['POST'])
def new_article():

    logger.info('访问 new_article 页面')
    
    title = 'next.js'
    content ='more...'
    tag = 'next.js, interview'
    user_id = 2333
    topic = 'fe'
    
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



# '127.0.0.1:9000/article/search?page_num=1&keyword=vue'
# 搜素文章
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
@main.route("/latest", methods=['GET'])
def latest():
    pass


# 点击推荐文章
@main.route("/recommend", methods=['GET'])
def recommend():
    pass

# # '127.0.0.1:9000/index?page_num=1&type=latest&topic=fe'
# @main.route("/index", methods=['GET'])
# def index():
#     logger.info('访问 index 页面')
    
#     page_num = request.args.get("page_num")
#     type = request.args.get("type")
#     topic = request.args.get("topic")
   
#     if page_num is None:
#         page_num = 1
#     else:
#         page_num = int(page_num)  

#     if type is None:
#         type ='recommend'
    
#     if topic is None:
#         topic = 'fe'
    
    
#     try:     
#         if type == "recommend":
#             total_count, total_pages, items = Article.query_recommend_article_by_page(page_num, topic)
#             return success(
#                 msg="success", data={'total_count': total_count, 'total_pages': total_pages, 'items': items})

#         else:
#             total_count, total_pages, items = Article.query_latest_article_by_page(page_num, topic)
#             return success(
#                 msg="success", data={'total_count': total_count, 'total_pages': total_pages, 'items': items})

#     except exc.SQLAlchemyError as e:
#         logger.error('query_{}_article_by_page error, {}'.format(type, e))
#         return error(code=HttpCode.db_error, msg="查询最新文章失败")
