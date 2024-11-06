
"""
通用

"""


import random

def random_str():
    """
    生成一个随机的字符串
    """
    seed = '@#$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


import random
import string

def random_code():
    # abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    seed = string.ascii_letters + string.digits
    # 取样
    sample = random.sample(seed, 6)
    # 拼接字符串
    return ''.join(sample).lower()



from datetime import datetime

def log(*args, **kwargs):
    """
    打印日志
    """
    # 获取当前日期和时间
    now = datetime.now()
    # 将其格式化为字符串, 例如 "2024/10/29 17:25:23"
    formatted_date = now.strftime('%Y/%m/%d %H:%M:%S')

    # 输出1
    print('<log>', formatted_date, *args, **kwargs)

    # 输出2
    with open('gua.log', 'a', encoding='utf-8') as f:
        print(formatted_date, *args, file=f, **kwargs)


"""
用法

log('gua')
"""


def hashed_password(plain_text):
    import hashlib
    # 用 ascii 编码转换成 bytes 对象
    p = plain_text.encode('ascii')
    s = hashlib.md5(p)
    # 返回摘要字符串
    return s.hexdigest()


def salted_password(password, salt='$!@><?>HUI&DWQa`'):
    
    def hashed_pwd(ascii_str):
        import hashlib
        return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

    hash1 = hashed_pwd(password)
    hash2 = hashed_pwd(hash1 + salt)
    return hash2



"""
发送邮件
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.log import logger

 
def send_email(to_email, subject, cc):
    """
    注册
    更改密码
    登录
    """
    from_email = ''
    license = ''  # 授权码
    content = "验证码：{}".format(cc)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    # 发送邮件正文，html格式的
    # msg.attach(MIMEText(content, "html", "utf-8"))    
    # 发送邮件正文，text格式的
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
    try:
        m = smtplib.SMTP_SSL("smtp.qq.com", 465) # 邮箱服务器及端口号
                
        m.login(from_email, license)
        m.sendmail(from_email, to_email, msg.as_string())
        m.close()        
        return True
    except Exception as e:
        logger.error("邮件发送失败, {}".format(e))
        return False
    finally:
        m.close()


import re


def validate_password(password):
    """
    验证密码是否符合要求：8-16位的英文字母、数字、字符组合（不能是纯数字）
    :param password: 要验证的密码字符串
    :return: 如果密码符合要求返回 True，否则返回 False
    """
    pattern = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9a-zA-Z!@#$%^&*()_+-=]{8,16}$')
    if re.match(pattern, password):
        return True
    return False
