from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

class APIKeyRequest(BaseModel):
    api_key: str

class APIKeyResponse(BaseModel):
    valid: bool

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(BaseModel):
    role: Role 
    content: str

class ChatRequest(BaseModel):
    chat_id: Optional[UUID] = Field(default_factory=uuid4)
    # api_key: str
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str
    context: Optional[str] = None