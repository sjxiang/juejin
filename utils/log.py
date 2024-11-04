import logging


# 通用配置
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(name)s - [%(levelname)s] - %(message)s')
log_level = logging.INFO


# 输出 1 stderr
_print_to_stderr = logging.StreamHandler()
_print_to_stderr.setFormatter(formatter)
_print_to_stderr.setLevel(log_level)

# 输出 2 file
_print_to_file = logging.FileHandler('logs/gua.log', mode='a')  # w, 会覆盖、 a, 会追加
_print_to_file.setFormatter(formatter)
_print_to_file.setLevel(log_level)

# 日志对象 <dev 使用>
logger = logging.getLogger('<log>')

# 添加日志记录器
logger.addHandler(_print_to_stderr)   
logger.addHandler(_print_to_file)      
logger.setLevel(log_level)         

logger.propagate = False              


"""
用法

from utils.log import logger

logger.info('test')
logger.error("test")

"""


