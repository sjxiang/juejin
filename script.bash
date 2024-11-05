

#!/bin/bash

# 定义要发送的JSON数据
json_data='{
    "email": "your_email@example.com",
    "password": "123456",
    "confirmed_password": "your_confirmed_password",
    "captcha_code": "aklrqh"
}'

# 使用curl命令发送POST请求，设置Content-Type头为application/json，并传递JSON数据
curl -X POST http://127.0.0.1:9000/user/register \
  -H "Content-Type: application/json" \
  -d "{
    "email": "your_email@example.com",
    "password": "123456",
    "confirmed_password": "your_confirmed_password",
    "captcha_code": "aklrqh"
}"

curl --location --request POST 'http://127.0.0.1:9000/user/register' \
--header "Content-Type: application/x-www-form-urlencoded" \
--data-raw "email=your_email@example.com&password=123456&confirmed_password=test_password&captcha_code=aklrqh"
{
    "email": "your_email@example.com",
    "password": "123456",
    "confirmed_password": "your_confirmed_password",
    "captcha_code": "aklrqh"
}'

#!/bin/bash

# 使用curl命令发送POST请求，设置Content-Type头为application/x-www-form-urlencoded
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=test_user&password=test_password" http://localhost:5000/submit_form