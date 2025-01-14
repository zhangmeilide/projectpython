import os
from fastapi import  HTTPException,UploadFile
from typing import List
import aiofiles
# 上传目录
UPLOAD_DIR = os.path.join(os.path.dirname(__file__),"..","uploads")

# 确保目录存在
os.makedirs(UPLOAD_DIR,exist_ok=True)

def save_file(file: UploadFile,file_name: str)->str:
    """
    保存文件到上传目录。
    :param file: 上传的文件对象
    :param file_name: 文件名
    :return: 文件路径
    """
    file_path = os.path.join(UPLOAD_DIR,file_name)
    try:
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
            # 返回相对路径，并确保使用正斜杠
            relative_path = os.path.join("uploads", file_name).replace("\\", "/")
            return relative_path  # 返回相对路径或URL路径
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败：{e}")

def save_files(files: List[UploadFile],file_names: List[str])->List[str]:
    """
    批量保存文件到上传目录。
    :param files: 上传的文件对象列表
    :param file_names: 文件名列表
    :return: 文件路径列表
    """
    if len(files) != len(file_names):
        raise HTTPException(status_code=400, detail="文件和文件名列表长度不匹配")

    file_paths = []
    for file,file_name in zip(files,file_names):
        file_path = save_file(file,file_name)
        file_paths.append(file_path)
    return  file_paths

def get_file_path(file_name: str) -> str:
    """
    获取文件路径。
    :param file_name: 文件名
    :return: 文件路径
    """
    file_path = os.path.join(UPLOAD_DIR,file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,detail="文件不存在")
    return file_path















