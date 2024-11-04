
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

