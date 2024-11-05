from flask import (
    Blueprint, request
)
from utils.log import logger
from models.article import Article


main = Blueprint('index', __name__)


# '127.0.0.1:9000/index?page=1&type=latest&topic=fe'
@main.route("/index", methods=['GET'])
def index():
    logger.info('访问 index 页面')
    
    raw_page = request.args.get("page")
    type = request.args.get("type")
    topic = request.args.get("topic")
   
    
    page = int(raw_page)
    
    if raw_page is None or (page < 1):
        page = 1
    
    if topic is None:
        topic = 'fe'
    if type is None:
        type ='recommend'
    
    
    if type == "recommend":
        response = Article.query_recommend_article_by_page(page, topic)
        return response
    else:
        response = Article.query_latest_article_by_page(page, topic)
        return response


# '127.0.0.1:9000/search?page=1&keyword=vue'
@main.route("/search", methods=['GET'])
def search():
    
    logger.info('访问 search 页面')
    
    raw_page = request.args.get("page")
    keyword = request.args.get("keyword")
    
    page = int(raw_page)
    
    if raw_page is None or (page < 1):
        page = 1
        
    response = Article.query_article_by_field(page, keyword=keyword)
    return response


"""
在 flask 中, 模块化路由的功能由 蓝图 (Blueprints) 提供
蓝图可以拥有自己的静态资源路径、模板路径 (现在还没涉及)
"""


"""
用法如下

from routes.user import main as user_routes
from routes.index import main as index_routes
app.register_blueprint(index_routes)
app.register_blueprint(user_routes, url_prefix='/user')


tips
    注册蓝图
    有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀

"""

