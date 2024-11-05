import enum

class ErrNo(enum.Enum):
    OK = 0
    
    # infra
    SERVER_ERROR = 10000
    DATABASE_ERROR = 10001
    DATABASE_RECORD_NOT_FOUND = 10002
    SEND_EMAIL_ERROR = 10003
    
    # biz
    RECORD_NOT_EXISTS = 20001
    RECORD_ALREADY_EXISTS = 20002
    
    # params
    PARAMS_INVALID = 30001
    
    

