
from flask import (
    Blueprint, request, render_template, session, jsonify
)
from utils.log import logger
from utils.common import random_num
# from models.user import UserInfo

import json
import re


main = Blueprint('user', __name__)


    # 填写原密码
    # 填写新密码
    # 再次填写确认
    
    # 密码必须是 8-16 位的英文字母、数字、字符组合(不能是纯数字)
    

# if PublicAdminController.check_phone_num(userInfo.user_id):
#     if len(userInfo.user_id) == 0 or len(userInfo.password) == 0:
#         return {"code": ErrorCode.USERID_OR_PASSWORD_ERROR.value, "message": "用户名或密码不能为空"}
#     else:
#         response = UserAdminCrud.query_user_by_userid(userInfo.user_id, db)
#         if response.get('code') == 0:
#             data = response.get('data')
#             if data is not None:
#                 return {"code": ErrorCode.USERID_ALREADY_EXISTS.value, "message": "用户名已存在"}
#             else:
#                 userInfo.password = get_password_hash(userInfo.password)
#                 return UserAdminCrud.add_user(userInfo, db)
#         else:
#             return response
# else:
#     return {"code": ErrorCode.USERID_NOT_INVALID.value, "message": "用户名不合法，格式为手机号"}

# import json
# import re
# from utils.log import hashed_password
# from models.user import User


# @main.route("/register",methods=["post"])
# def register():
#     request_data = json.loads(request.data)
    
#     email = request_data.get("email")
#     password = request_data.get("password")
#     confirmed_password = request_data.get("confirmed_password")
    
#     print(email, password, confirmed_password)

#     # 数据校验
#     if not re.match(".+@.+\..+", email):
#         return '无效邮箱'
#     if len(password) < 6:
#         return '密码太短'
#     if password != confirmed_password:
#         return '两次密码不一致'
    
    
#     if User.find_one_by_email(input_email=email) is not None:
#         return '用户已存在'
    
#     new_user = {
#         "email":    email,
#         "nickname": email.split("@")[0],
#         "password": hashed_password(password)
#     }
#     if User.create(**new_user) is not None:
#         return '用户注册成功'
#     else:
#         return '数据库繁忙'


# 获取验证码 <邮箱替代短信>
@main.route("/sms-code", methods=['GET'])
def send_sms():
    logger.info('访问 sms-code 页面')
    
    code = random_num()
    session['code'] = code
    
    logger.info('验证码: {}'.format(code))

    return jsonify(code=code)    



@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        logger.info('访问 login 页面')
        return render_template("login.html")
    
    pass


@main.route("/register", methods=['POST'])
def register():
    pass

    # request_data = json.loads(request.data)
    
    # email = request_data.get("email")
    # password = request_data.get("password")
    # confirmed_password = request_data.get("confirmed_password")
    
        
    # # 数据校验
    # if not re.match(".+@.+\..+", email):
    #     return '无效邮箱'
    # if len(password) < 6:
    #     return '密码太短'
    # if password != confirmed_password:
    #     return '两次密码不一致'
    
   
    # if User.find_one_by_email(email=email) is not None:
    #     return '用户已存在'
    
    # new_user = {
    #     "email":    email,
    #     "nickname": email.split("@")[0],
    #     "password": hashed_password(password)
    # }
    # if User.create(new_user) is not None:
    #     return '用户注册成功'


# @user.route("/reg",methods=["post"])
# def register():
#     request_data = json.loads(request.data)
#     username = request_data.get("username")
#     password = request_data.get("password")
#     second_password = request_data.get("second_password")
#     ecode = request_data.get("ecode")
#     # 数据验证
#     if ecode.lower() != session.get("ecode"):
#         return response_message.UserMessage.error("邮箱验证码错误")
#     if not re.match(".+@.+\..+",username):
#         return response_message.UserMessage.other("无效邮箱")
#     if len(password) < 6:
#         return response_message.UserMessage.error("密码不合格")
#     if password != second_password:
#         return response_message.UserMessage.error("两次密码不一致")
#     user = User()
#     if user.find_dy_suername(username=username) is not None:
#         return response_message.UserMessage.error("用户已存在")
#     # 实现注册的功能了
#     password = hashlib.md5(password.encode()).hexdigest()
#     result = user.bo_register(username,password)
#     return response_message.UserMessage.success("用户注册成功")

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

# # 注销功能的实现
# @user.route("/logout")
# def logout():
#     # 清空session
#     session.clear()
#     response = make_response("注销并进行重定向", 302)
#     # 这里的url_for写的不是一个url地址,而是我们的控制器的模块名称.函数名称，然后映射到这个控制器处理函数的地址上
#     response.headers["Location"] = url_for("index.home")
#     # 清除掉cookie
#     response.delete_cookie("username")
#     return response
