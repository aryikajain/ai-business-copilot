# Chat routes will be implemented here
from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.rag_service import get_rag_context
from rag.prompts import build_business_prompt
from rag.llm import generate_response


router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    query: str


@router.post("/")
def chat_with_business_ai(request: ChatRequest):
    # 1. retrieve relevant business memory
    context = get_rag_context(request.user_id, request.query)

    # 2. build business-aware prompt
    prompt = build_business_prompt(context, request.query)

    # 3. generate answer
    answer = generate_response(prompt)

    return {
        "query": request.query,
        "context": context,
        "answer": answer
    }