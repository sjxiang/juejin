from flask import (
    Blueprint, request
)
from utils.log import logger
from models.article import Article
from sqlalchemy import exc
from utils.serializer import HttpCode, success, error

main = Blueprint('index', __name__)


# '127.0.0.1:9000/index?page_num=1&type=latest&topic=fe'
@main.route("/index", methods=['GET'])
def index():
    logger.info('访问 index 页面')
    
    page_num = request.args.get("page_num")
    type = request.args.get("type")
    topic = request.args.get("topic")
   
    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)  

    if type is None:
        type ='recommend'
    
    if topic is None:
        topic = 'fe'
    
    
    try:     
        if type == "recommend":
            total_count, total_pages, items = Article.query_recommend_article_by_page(page_num, topic)
            return success(
                msg="success", data={'total_count': total_count, 'total_pages': total_pages, 'items': items})

        else:
            total_count, total_pages, items = Article.query_latest_article_by_page(page_num, topic)
            return success(
                msg="success", data={'total_count': total_count, 'total_pages': total_pages, 'items': items})

    except exc.SQLAlchemyError as e:
        logger.error('query_{}_article_by_page error, {}'.format(type, e))
        return error(code=HttpCode.db_error, msg="查询最新文章失败")



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

