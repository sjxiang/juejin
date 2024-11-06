from flask import (
    Blueprint, render_template
)
from utils.log import logger


main = Blueprint('index', __name__)

# 首页
# '127.0.0.1:9000/index'
@main.route("/index", methods=['GET'])
def index():
    logger.info('访问 index 页面')
    return render_template("index.html")



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

