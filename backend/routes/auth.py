from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database.crud import get_user_by_email, create_user
from backend.services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter()

# 🧠 Request schema (important)
class UserAuth(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(user: UserAuth):

    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    create_user({
        "email": user.email,
        "password": hashed_password
    })

    return {
        "status": "success",
        "message": "User registered successfully"
    }


@router.post("/login")
def login(user: UserAuth):

    db_user = get_user_by_email(user.email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "user_id": str(db_user["_id"]),
        "email": db_user["email"]
    })

    return {
        "status": "success",
        "access_token": token,
        "user": {
            "email": db_user["email"]
        }
    }