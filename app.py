from flask import Flask

from utils.config import config
from utils.consts import env
from routes.user import main as user_routes
from routes.index import main as index_routes

app = Flask(__name__, template_folder='templates')

cfg = config[env]
    
# 设置 secret_key 来使用 flask 自带的 session
app.secret_key = cfg.SECRET_KEY

# 注册蓝图
app.register_blueprint(index_routes)
app.register_blueprint(user_routes, url_prefix='/user')

# from routes.topic import main as topic_routes
# from routes.reply import main as reply_routes
# from routes.board import main as board_routes
# from routes.mail import main as mail_routes
# app.register_blueprint(topic_routes, url_prefix='/topic')
# app.register_blueprint(reply_routes, url_prefix='/reply')
# app.register_blueprint(board_routes, url_prefix='/board')
# app.register_blueprint(mail_routes, url_prefix='/mail')
    

# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=9000,
    )    
    app.run(**config)
