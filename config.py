
# 配置
sql_host = '127.0.0.1'
sql_port = 13306
sql_username = 'root'
sql_password = 'my-secret-pw'
sql_db = 'juejin_community'

database_url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(sql_username, sql_password, sql_host, sql_port, sql_db)
secret_key = 'juejin'


# if __name__ == "__main__":
#     from models.user import User

#     # data = User.new("15354@qq.com", "123456")
#     # print(data)
    
#     data = User.find_one_by_email("15354@qq.com")
#     print(data)
#     print(data.password)



