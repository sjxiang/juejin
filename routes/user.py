
from flask import (
    Blueprint, request, render_template, session
)
from sqlalchemy import exc

from utils.bootstrap import redis_connect
from utils.log import logger
from utils.common import random_code, send_email, validate_password, hashed_password
from models.user import User
from utils.serializer import HttpCode, success, error
import json
import re


# 连接 redis
rds = redis_connect()

main = Blueprint('user', __name__)


# 获取短信验证码 <邮箱替代短信>
@main.route("/sms-code", methods=['POST'])
def sms_code():
    to_email = json.loads(request.data).get("email")
    
    # 简单的邮箱格式验证
    if not re.match(".+@.+\..+", to_email):
        return error(code=HttpCode.params_error, msg="邮箱格式错误")
    
    # 生成邮箱验证码的随机字符串
    cc = random_code()
    
    # 将邮箱验证码存入 redis 
    prefix = 'captcha_code_'
    rds.set(prefix+to_email, cc, ex=60*10)
    
    # 发送邮件
    logger.info('邮箱验证码: {}'.format(cc))
    
    return success(msg="发送成功")

    # is_success = send_email(to_email, "注册", cc)
    # if is_success:
    #     return success(msg="发送成功")
    # else:
    #     return error(code=HttpCode.server_error, msg="发送失败")


@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        logger.info('访问 login 页面')
        return render_template("login.html")
    
    pass


@main.route("/register", methods=['POST'])
def register():
    data = json.loads(request.data)
    
    email = data.get("email")
    password = data.get("password")
    confirmed_password = data.get("confirmed_password")
    captcha_code = data.get("captcha_code")
        
    if not re.match(".+@.+\..+", email):
        return error(code=HttpCode.params_error, msg="邮箱格式错误")
    if not all([email, password, confirmed_password, captcha_code]):
        return error(code=HttpCode.params_error, msg='参数不能为空')
    if captcha_code != rds.get('captcha_code_'+email):
        return error(code=HttpCode.params_error, msg='验证码错误')
    if password != confirmed_password:
        return error(code=HttpCode.params_error, msg='两次密码不一致')
    if validate_password(password):
        return error(code=HttpCode.params_error, msg='密码不合格')

    
    try:
        item = User.query_user_by_email(email=email)
    
        if item is None:
            new_user = {
                "email": email,
                "nickname": email.split("@")[0],
                "password": hashed_password(password)
            }

            User.new(**new_user)
            return success(msg='注册成功')
        else:
            return error(code=HttpCode.record_already_exists, msg='用户已存在')
        
    except exc.SQLAlchemyError as e:
        logger.error('query_user_by_email error {}, email, {}'.format(e, email))
        return error(code=HttpCode.db_error, msg='注册失败')
    

# @user.route("/login",methods=["post"])
# def login():
#     request_data = json.loads(request.data)
#     username = request_data.get("username")
#     password = request_data.get("password")
#     vcode = request_data.get("vcode")

#     if vcode != session.get("vcode"):
#         return response_message.UserMessage.error("验证码输入错误")
#     #实现登录功能
#     password = hashlib.md5(password.encode()).hexdigest()
#     user = User()
#     result = user.find_dy_suername(username)
#     if len(result) == 1 and result[0].password==password:
#         # 需要进行登录状态的管理
#         session["is_login"]="true"
#         session["user_id"] = result[0].user_id
#         session["username"] = username
#         session["nickname"] = result[0].nickname
#         session["picture"] = config[env].user_header_image_path+result[0].picture

#         response=make_response(response_message.UserMessage.success("登录成功"))
#         response.set_cookie("username",username,max_age=30*24*3600)
#         return response
#     else:
#         return response_message.UserMessage.error("用户名或者是密码错误")




# 注销
@main.route("/logout")
def logout():
    # 清空 session
    session.clear()
    
    # response = make_response("注销并进行重定向", 302)
    # # 这里的url_for写的不是一个url地址,而是我们的控制器的模块名称.函数名称，然后映射到这个控制器处理函数的地址上
    # response.headers["Location"] = url_for("index.home")
    # # 清除掉cookie
    # response.delete_cookie("username")
    # return response


@main.route("/reset-password", methods=['POST'])
def reset_password():
    
    # 填写原密码
    # 填写新密码
    # 再次填写确认
    # 密码必须是 8-16 位的英文字母、数字、字符组合(不能是纯数字)
    
    pass

