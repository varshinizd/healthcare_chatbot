from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


# ── Auth ──────────────────────────────────────────────────────────────────────

class SignupRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    # Health profile
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=1, le=500)
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    smoking_status: Optional[str] = None
    alcohol_status: Optional[str] = None
    # Conditions
    condition_ids: List[str] = []
    custom_conditions: List[str] = []


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ConditionOut(BaseModel):
    id: int
    condition_name: str
    is_custom: bool

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    blood_group: Optional[str]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    allergies: Optional[str]
    current_medications: Optional[str]
    smoking_status: Optional[str]
    alcohol_status: Optional[str]
    conditions: List[ConditionOut] = []

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=1, le=500)
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    smoking_status: Optional[str] = None
    alcohol_status: Optional[str] = None
    condition_ids: List[str] = []
    custom_conditions: List[str] = []


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    blocked: bool = False
    block_reason: Optional[str] = None
    is_emergency: bool = False
    category: str = "unknown"
    rag_used: bool = False
    latency_ms: float = 0.0
    message_id: str
    is_clarifying_question: bool = False


# ── Feedback ──────────────────────────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    session_id: str
    message_id: str
    score: int = Field(..., ge=-1, le=1)
    comment: Optional[str] = Field(None, max_length=500)


class FeedbackResponse(BaseModel):
    success: bool
    message: str


# ── Health ────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    app_name: str
    rag_ready: bool
    uptime_seconds: float
