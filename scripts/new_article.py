import requests
import json


url = "http://127.0.0.1:9000/article/new"

payload = {
    "title": "auto-testing",
    "content": "more...",
    "tag": "interview, testing",
    "topic": "test"
}
 
headers = {
    "Content-Type": "application/json"
}  

try:
    # 发送POST请求
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
        
    # 检查响应状态码，如果状态码为200，表示请求成功
    if response.status_code == 200:
        print("请求成功，响应内容如下：")
        print(json.loads(response.text))
    else:
        print(f"请求失败，状态码：{response.status_code}，响应内容：{json.loads(response.text)}")

except requests.exceptions.RequestException as e:
    print(f"请求过程中出现错误：{e}")
    