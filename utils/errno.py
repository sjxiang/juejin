import enum

class ErrNo(enum.Enum):
    OK = 0
    
    # infra
    SERVER_ERROR = 10000
    DATABASE_ERROR = 10001
    SEND_EMAIL_ERROR = 10002
    
    # biz
    USER_NOT_EXISTS = 20001
    USER_ALREADY_EXISTS = 20002
    
    # params
    PARAMS_INVALID = 30001
    
    

