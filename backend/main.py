from fastapi import FastAPI
from backend.routes import auth,upload,chat

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
@app.get("/")
def root():
    return {"msg": "AI Business Copilot running"}