import http.client
import json
import ssl
import os


class VsmApiService:
    def __init__(self):
        self.base_url = "192.168.234.18:28001"
        self.res_id = "668daf6a-a54f-4ae0-8d69-69084f62c21a"
        self.app = "5fd8e53d-cfcb-4ca9-8159-ebccb78b872f"
        self.password = "1qaz@WSX"
        self.user = ""
        self.token = None
        self.url_prefix = f"/vsm/{self.res_id}/api/1/key"
        self.short_key = os.path.exists("conf.conf")

    def open_device(self, app: str, user: str, password: str):
        self.token = self._post_json(
            "/auth/api/1/auth/login",
            {
                "app": app,
                "user": user,
                "password": password
            }
        ).get("data")

    def open_device_bak(self, *_):
        self.token = self._post_json(
            "/auth/api/1/auth/login",
            {
                "app": self.app,
                "user": self.user,
                "password": self.password
            }
        ).get("data")

    def close_device(self):
        self._post_json("/auth/api/1/auth/logout", data={}, headers=self._auth_header())

    def encrypt(self, key_id, key_alias, in_data):
        return self.send("/encrypt", {"keyId": key_id, "keyAlias": key_alias, "inData": in_data})

    def decrypt(self, ciphertext):
        return self.send("/decrypt", {"inData": ciphertext})

    def hmac_sm3(self, key_id, key_alias, in_data):
        url = "/hmacShorter" if self.short_key else "/hmac"
        return self.send(url, {"keyId": key_id, "keyAlias": key_alias, "inData": in_data})

    def sign(self, key_id, key_alias, in_data):
        return self.send("/sign", {"keyId": key_id, "keyAlias": key_alias, "inData": in_data})

    def verify(self, key_id, key_alias, in_data, signature):
        return self.send("/verify", {"keyId": key_id, "keyAlias": key_alias, "inData": in_data, "signature": signature})

    def random(self, length):
        return self.send("/random", {"randomLen": length})

    def sign_external(self, private_key, in_data):
        return self.send("/signExternal", {"privateKey": private_key, "inData": in_data})

    def verify_external(self, public_key, in_data, signature):
        return self.send("/verifyExternal", {"publicKey": public_key, "inData": in_data, "signature": signature})

    def generate_envelop(self, file_path, cert, output_path):
        # multipart/form-data 上传文件功能略复杂，不建议用 http.client 实现
        raise NotImplementedError("需要实现 multipart/form-data 文件上传逻辑")

    def open_envelop(self, envelop_path, cert, output_path):
        raise NotImplementedError("需要实现 multipart/form-data 文件上传逻辑")

    def send(self, path, data):
        return self._post_json(self.url(path), data, headers=self._auth_header()).get("data")

    def _auth_header(self):
        return {"token": self.token} if self.token else {}

    def url(self, path):
        return f"{self.url_prefix}{path}"

    def _post_json(self, path, data, headers=None):
        conn = http.client.HTTPSConnection(self.base_url, context=ssl._create_unverified_context())
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        json_data = json.dumps(data)

        print(f"请求: POST {path}")
        conn.request("POST", path, body=json_data, headers=headers)

        response = conn.getresponse()
        body = response.read().decode("utf-8")

        if response.status >= 400:
            raise Exception(f"请求失败: {response.status}, 内容: {body}")

        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise Exception("响应不是合法 JSON: " + body)
