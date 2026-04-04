from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from backend.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Extended health profile
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    allergies = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    smoking_status = Column(String, nullable=True)
    alcohol_status = Column(String, nullable=True)

    conditions = relationship("UserCondition", back_populates="user", cascade="all, delete-orphan")
    chat_events = relationship("ChatEvent", back_populates="user", cascade="all, delete-orphan")


class UserCondition(Base):
    __tablename__ = "user_conditions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    condition_name = Column(String, nullable=False)
    is_custom = Column(Boolean, default=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conditions")


class ChatEvent(Base):
    __tablename__ = "chat_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String, nullable=False)
    message_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    query_hash = Column(String)
    query_category = Column(String)
    was_blocked = Column(Boolean, default=False)
    block_layer = Column(String, nullable=True)
    response_length = Column(Integer)
    latency_ms = Column(Float)
    rag_used = Column(Boolean, default=False)
    feedback_score = Column(Integer, nullable=True)
    is_emergency = Column(Boolean, default=False)

    user = relationship("User", back_populates="chat_events")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
