from fastapi import UploadFile,HTTPException
from utils.file_utils import save_file,get_file_path,save_files
from typing import List

def upload_file(file: UploadFile):
    """
    处理文件上传逻辑。
    :param file: 上传的文件对象
    :return: 文件路径
    """
    return save_file(file,file.filename)

def download_file(filename: str)->str:
    """
    处理文件下载逻辑。
    :param file_name: 文件名
    :return: 文件路径
    """
    return get_file_path(filename)

def upload_files(files: List[UploadFile], file_names: List[str]) -> List[str]:
    return save_files(files, file_names)






