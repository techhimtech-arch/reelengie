from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List

from app.services.upload_service import upload_service

router = APIRouter()

@router.post("/{project_id}/media/{media_type}")
async def upload_media(project_id: str, media_type: str, file: UploadFile = File(...)):
    if media_type not in ["videos", "photos", "voice"]:
        raise HTTPException(status_code=400, detail="Invalid media type. Must be videos, photos, or voice.")
        
    try:
        file_path = upload_service.save_file(project_id, media_type, file)
        return {"status": "success", "file": file.filename, "path": file_path}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

class ScriptRequest(BaseModel):
    content: str

@router.post("/{project_id}/script")
async def upload_script(project_id: str, request: ScriptRequest):
    try:
        file_path = upload_service.save_script(project_id, request.content)
        return {"status": "success", "message": "Script saved."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
