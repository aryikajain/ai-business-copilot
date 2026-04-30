# # File upload routes will be implemented here
# from fastapi import APIRouter, UploadFile, File, HTTPException
# from backend.services.file_service import save_file
# from backend.services.processing_service import process_file
# from backend.services.rag_service import build_rag_memory
# from backend.database.db import uploads_collection

# from jose import jwt


# router = APIRouter()

# SECRET_KEY = "supersecretkey"
# ALGORITHM = "HS256"



# def get_user_id_from_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload.get("user_id")
#     except:
#         return None


# @router.post("/")
# def upload_file(file: UploadFile = File(...), token: str = ""):

#     user_id = get_user_id_from_token(token)

#     if not user_id:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     file_path = save_file(user_id, file)

#     uploads_collection.insert_one({
#         "user_id": user_id,
#         "file_name": file.filename,
#         "file_path": file_path
#     })
#     result = process_file(file_path)

#     return {
#         "status": "success",
#         "file_path": file_path,
#         "analysis": result

#     }

#     # build RAG memory
#     build_rag_memory(user_id, result)
    
from fastapi import APIRouter, UploadFile, File, HTTPException
from jose import jwt
from backend.services.file_service import save_file
from backend.services.processing_service import process_file
from backend.services.rag_service import build_rag_memory
from backend.database.db import uploads_collection

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


def get_user_id_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
    except:
        return None


@router.post("/")
def upload_csv(file: UploadFile = File(...), token: str = ""):
    user_id = get_user_id_from_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 1. save file
    file_path = save_file(user_id, file)

    # 2. process file
    analysis = process_file(file_path)

    # 3. save upload metadata
    uploads_collection.insert_one({
        "user_id": user_id,
        "file_name": file.filename,
        "file_path": file_path
    })

    # 4. build RAG memory
    build_rag_memory(user_id, analysis)

    # 5. return response
    return {
        "status": "success",
        "file_path": file_path,
        "analysis": analysis
    }