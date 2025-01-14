from fastapi import APIRouter,File,UploadFile,HTTPException
from fastapi.responses import FileResponse
from services.file_service import upload_file,download_file,upload_files
from typing import List

router = APIRouter()

@router.post('/upload/')
async def upload(file: UploadFile):
    """
    上传文件接口。
    """
    file_path = upload_file(file)
    return {"message": "文件上传成功", "file_path": file_path}

@router.get("/download/{file_name}")
async def download(file_name: str):
    """
    下载文件接口。
    """
    file_path = download_file(file_name)
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)

@router.post("/upload/multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...), file_names: List[str] = File(...)):
    print(files)
    print(file_names)
    """
    批量上传文件接口。
    """
    try:
        file_paths = upload_files(files, file_names)
        return {"message": "文件上传成功", "file_paths": file_paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败：{e}")