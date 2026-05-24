from fastapi import APIRouter, File, HTTPException, UploadFile
from jose import jwt

from backend.database.db import uploads_collection
from backend.services.file_service import save_file
from backend.services.processing_service import process_file
from backend.services.rag_service import build_rag_memory

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


def get_user_id_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
    except Exception:
        return None


@router.post("/")
def upload_csv(file: UploadFile = File(...), token: str = ""):
    user_id = get_user_id_from_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    file_path = save_file(user_id, file)
    analysis = process_file(file_path)

    uploads_collection.insert_one(
        {
            "user_id": user_id,
            "file_name": file.filename,
            "metrics": analysis.get("metrics", {}),
            "insights": analysis.get("insights", []),
            "debug": analysis.get("debug", {}),
            "clusters": analysis.get("clusters", {}),
        }
    )

    build_rag_memory(user_id, analysis)

    return {
        "status": "success",
        "file_path": file_path,
        "analysis": analysis,
    }
