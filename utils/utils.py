
import time
import random


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('gua.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)



def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefghijklmnopqrstuvwxyz0123456789'

    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def hashed_password(input_password):
    import hashlib
    # 用 ascii 编码转换成 bytes 对象
    p = input_password.encode('ascii')
    s = hashlib.md5(p)
    # 返回摘要字符串
    return s.hexdigest()


def salted_password(input_password, salt='$!@><?>HUI&DWQa`'):
    
    def hashed_pwd(ascii_str):
        import hashlib
        return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

    hash1 = hashed_pwd(input_password)
    hash2 = hashed_pwd(hash1 + salt)
    return hash2