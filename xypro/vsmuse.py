# vsm_api.py
# 由于 VsmApiService 是未知导入符号，暂时注释掉该导入语句，需要确认 vsm_service 模块是否存在以及路径是否正确
from vsm_service import VsmApiService
import json

def create_vsm():
    vsm = VsmApiService()
    vsm.open_device("5fd8e53d-cfcb-4ca9-8159-ebccb78b872f", "admin", "1qaz@WSX")
    return vsm

def encrypt_text(text: str):
    vsm = create_vsm()
    encrypted = vsm.encrypt("d42e7d91-62ff-4ba2-a3fd-90fa2198c8a1", "sed- xyzhjg", text)
    return {
        "status": 200,
        "message": "加密成功",
        "encrypted_str": encrypted
    }

def decrypt_text(ciphertext: str):
    vsm = create_vsm()
    decrypted = vsm.decrypt(ciphertext)
    return {
        "status": 200,
        "message": "解密成功",
        "decrypted_str": decrypted
    }

def get_random_bytes(length: int = 16):
    vsm = create_vsm()
    random_bytes = vsm.random(length)
    return {
        "status": 200,
        "message": "获取随机数成功",
        "randomB": random_bytes
    }

def verify_external_signature(public_cert: str, in_data: str, signature: str):
    vsm = create_vsm()
    result = vsm.verify_external(public_cert, in_data, signature)
    return {
        "status": 200,
        "message": "验签成功",
        "verify_result": result
    }


if __name__ == "__main__":
    encrypt_res = encrypt_text("hello world")
    encrypted_str = encrypt_res.get("encrypted_str")
  
    print("加密结果:", json.dumps(encrypt_res, indent=2, ensure_ascii=False))
    if encrypted_str is not None:
        decrypt_res = decrypt_text(encrypted_str)
        print("解密结果:", json.dumps(decrypt_res, indent=2, ensure_ascii=False))
    else:
        print("encrypted_str 为 None，无法进行解密操作")
    
    print("随机数:", json.dumps(get_random_bytes(), indent=2, ensure_ascii=False))

    cert = """-----BEGIN CERTIFICATE-----
    MIIBZDCCAW+gLm66y3RTRwIhALIE5CSZpQv0J8hEv4ABnDDLhhZweT9Fsdx+QalgWFWr
    WIBAgIICu9Y/+t5SHEWDAYIKOECZ1UBg3UFADBDMQSWCQYDVQQGEWJDTjEel
    BwGCSgGSIb3DOEJARYPYWRtaW
    -----END CERTIFICATE-----"""

    in_data = "39C8A4AE784639C4D4F9A113526B7EEB"
    signature = "MEYCIOCD8ZNx/jAg60vVAC9HRZqasczk6A+sp4F"

    res = verify_external_signature(cert, in_data, signature)
    print(res)










