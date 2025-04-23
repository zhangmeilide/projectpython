import http.client
import json
print("脚本开始执行...")
host = "hyjgapi.scwljg.com"
endpoint = "/api/v1/vsmapi/test"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}

# 使用 HTTP（注意不是 HTTPS）
conn = http.client.HTTPConnection(host)

# 发起 POST 请求
conn.request("POST", endpoint, body=json.dumps(payload), headers=headers)

# 获取响应
response = conn.getresponse()
print("状态码:", response.status)

# 读取并解析响应内容
data = response.read().decode("utf-8")
try:
    json_data = json.loads(data)
    print("响应数据:", json_data)
except json.JSONDecodeError:
    print("响应内容不是合法的 JSON:", data)

# 关闭连接
conn.close()
