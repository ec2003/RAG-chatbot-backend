from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from src.models.models import ChatMessage, ChatRequest, ChatResponse, APIKeyRequest, APIKeyResponse
from src.chat import chat_with_milvus
from src.api_key_verifier import verify_api_key

app = FastAPI()

load_dotenv(".env")

API_KEYS = os.getenv("GOOGLE_API_KEYS").split(",") if os.getenv("GOOGLE_API_KEYS") else None
if API_KEYS is None: 
    raise ValueError("GOOGLE_API_KEYS environment variable not set")
CLUSTER_ENDPOINT = os.getenv("CLUSTER_ENDPOINT")
TOKEN = os.getenv("TOKEN")
if CLUSTER_ENDPOINT is None or TOKEN is None:
    raise ValueError("CLUSTER_ENDPOINT or TOKEN environment variable not set")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/verify_api_key", response_model=APIKeyResponse)
# async def verify_api_key_endpoint(api_key: APIKeyRequest):
#     _api_key = api_key.api_key
#     return APIKeyResponse(valid=verify_api_key(_api_key))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    question = chat_request.messages[-1].content
    chat_history = [msg.model_dump() for msg in chat_request.messages[:-1]]

    current_api_key = None
    for api_key in API_KEYS:
        if verify_api_key(api_key):
            current_api_key = api_key
            break
    if current_api_key is None:
        raise HTTPException(status_code=503, detail="No valid API Key available to process the request.")

    response, context = chat_with_milvus(question, 
                                         current_api_key, 
                                         chat_history,
                                         CLUSTER_ENDPOINT,
                                         TOKEN)
    return ChatResponse(response=response, context=context)

# @app.post("/chat/{chat_id}/", response_model=ChatResponse)
# async def chat_endpoint(chat_id: str, chat_request: ChatRequest):
#     question = chat_request.messages[-1].content
#     chat_history = [msg.model_dump() for msg in chat_request.messages[:-1]]
#     response, context = chat_with_milvus(question, chat_history)
#     return ChatResponse(response=response, context=context)
    