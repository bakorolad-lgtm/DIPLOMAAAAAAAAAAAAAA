from fastapi import APIRouter, UploadFile
from fastapi.params import Depends

from src.clients.s3 import S3Client
from src.utils import role_required

router = APIRouter(prefix="/files")

@router.post("")
async def save_file(file: UploadFile, user: dict = Depends(role_required("admin"))):
    S3Client("minio-files").upload_file(file.file, f"{user['id']}/{file.filename}")
    return {
        "file_url": f"http://localhost:9002/minio-files/{user['id']}/{file.filename}"
    }
