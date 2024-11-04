from flask import (
    Blueprint, request
)
from utils.log import logger


main = Blueprint('index', __name__)


@main.route("/index/recommend")
def index():
    logger.info('访问 index 推荐页面')
    
    raw_page = request.args.get("page")
    raw_label = request.args.get("label")

    page = int(raw_page)
    
    if raw_page is None or (page < 1):
        page = 1
    if raw_label is None:
        raw_label = "recommend"
        
    
    # 文章搜索功能实现
    search_keyword = request.args.get("keyword")
    if search_keyword is not None:
    
        db_result = article.search_article(page, search_keyword)
    else:
        db_result = article.find_article(page, article_type)
    for article,nickname in db_result:
        # 分类内容显示的转换
        article.label = label_types.get(article.label_name).get("name")
        # 日期的显示
        article.create_time = str(article.create_time.month) + '.' + str(article.create_time.day)
        # 图片路径的处理  "/images/article/header/"
        article.article_image = config[env].article_header_image_path + str(article.article_image)
        # 文章标签格式的修改
        article.article_tag = article.article_tag.replace(",", " · ")
        start_num = request.args.get("start_num")
    if start_num is None:
        start_num=0
    end_num = len(db_result)
    # 左侧菜单栏文章分类的逻辑
    for k,v in label_types.items():
        if article_type == k:
            v["selected"] = "selected"
        else:
            v["selected"] = "np-selected"
    return render_template("index.html",
                           result=db_result,
                           start_num=start_num,
                           end_num=end_num,
                           label_types=label_types)


# 对应前端显示分类的字典
label_types = {
    "recommend":{"name":"推荐","selected":"selected"},
    "auto_test":{"name":"自动化测试","selected":"no-selected"},
    "python":{"name":"Python","selected":"no-selected"},
    "java":{"name":"Java","selected":"no-selected"},
    "function_test":{"name":"功能测试","selected":"no-selected"},
    "perf_test":{"name":"性能测试","selected":"no-selected"},
    "funny":{"name":"幽默段子","selected":"no-selected"},
}




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

