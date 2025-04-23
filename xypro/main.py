from fastapi import FastAPI, Request
from vsm_service import VsmApiService

app = FastAPI()

def create_vsm():
    vsm = VsmApiService()
    vsm.open_device("5fd8e53d-cfcb-4ca9-8159-ebccb78b872f", "admin", "1qaz@WSX")
    return vsm

@app.post("/encrypt")
async def encrypt_text(request: Request):
    body = await request.json()
    text = body.get("text", "")
    vsm = create_vsm()
    encrypted = vsm.encrypt("d42e7d91-62ff-4ba2-a3fd-90fa2198c8a1", "sed- xyzhjg", text)
    return {"status": 200, "message": "加密成功", "encrypted_str": encrypted}

@app.post("/decrypt")
async def decrypt_text(request: Request):
    body = await request.json()
    ciphertext = body.get("ciphertext", "")
    vsm = create_vsm()
    decrypted = vsm.decrypt(ciphertext)
    return {"status": 200, "message": "解密成功", "decrypted_str": decrypted}

@app.post("/random")
async def get_random_bytes(request: Request):
    body = await request.json()
    length = body.get("length", 16)
    vsm = create_vsm()
    random_bytes = vsm.random(length)
    return {"status": 200, "message": "获取随机数成功", "randomB": random_bytes}

@app.post("/verify-external")
async def verify_external_signature(request: Request):
    body = await request.json()
    public_cert = body.get("public_cert", "")
    in_data = body.get("in_data", "")
    signature = body.get("signature", "")
    vsm = create_vsm()
    result = vsm.verify_external(public_cert, in_data, signature)
    return {"status": 200, "message": "验签成功", "verify_result": result}
