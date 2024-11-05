from flask import jsonify

# serializer

class HttpCode(object):
    ok = 200    
    params_error = 400
    server_error = 500
    auth_error = 401
    db_error = 1001
    record_already_exists = 1002
    record_not_exists = 1003
    

def response(code, msg, data):
    return jsonify(code=code, msg=msg, data=data or {})


def success(msg, data=None):
    # {code=200, msg='ok', data={}}
    return response(code=HttpCode.ok, msg=msg, data=data)


def error(code, msg, data=None):
    return response(code=code, msg=msg, data=data)
