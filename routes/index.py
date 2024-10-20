
from flask import (
    Blueprint, request
)

from utils.utils import hashed_password
from models.user import User

import json
import re

main = Blueprint('index', __name__)

@main.route("/")
def index():
    return 'welcome!'

@main.route("/register",methods=["post"])
def register():
    request_data = json.loads(request.data)
    
    email = request_data.get("email")
    password = request_data.get("password")
    confirmed_password = request_data.get("confirmed_password")
    
    print(email, password, confirmed_password)

    # 数据校验
    if not re.match(".+@.+\..+", email):
        return '无效邮箱'
    if len(password) < 6:
        return '密码太短'
    if password != confirmed_password:
        return '两次密码不一致'
    
    
    if User.find_one_by_email(input_email=email) is not None:
        return '用户已存在'
    
    new_user = {
        "email":    email,
        "nickname": email.split("@")[0],
        "password": hashed_password(password)
    }
    if User.create(**new_user) is not None:
        return '用户注册成功'
    else:
        return '数据库繁忙'


@main.route("/login", methods=['POST'])
def login():
    
    return '登录成功'
