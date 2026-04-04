from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.models.database import get_db, User, UserCondition
from backend.models.schemas import (
    SignupRequest, LoginRequest, TokenResponse,
    UserOut, UpdateProfileRequest,
)
from backend.models.conditions import PREDEFINED_CONDITIONS, CONDITION_IDS
from backend.core.auth import (
    hash_password, verify_password, create_access_token, get_current_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])

CONDITION_LABEL_MAP = {c["id"]: c["label"] for c in PREDEFINED_CONDITIONS}


def _sync_conditions(db: Session, user: User, condition_ids: list[str], custom_conditions: list[str]):
    db.query(UserCondition).filter(UserCondition.user_id == user.id).delete()
    for cid in condition_ids:
        if cid in CONDITION_IDS:
            db.add(UserCondition(
                user_id=user.id,
                condition_name=CONDITION_LABEL_MAP[cid],
                is_custom=False,
            ))
    for custom in custom_conditions:
        custom = custom.strip()
        if custom:
            db.add(UserCondition(
                user_id=user.id,
                condition_name=custom,
                is_custom=True,
            ))
    db.commit()


def _apply_profile_fields(user: User, req):
    """Apply all extended profile fields from a request object to a User."""
    fields = [
        "full_name", "age", "gender", "blood_group",
        "height_cm", "weight_kg", "allergies",
        "current_medications", "smoking_status", "alcohol_status",
    ]
    for field in fields:
        val = getattr(req, field, None)
        if val is not None:
            setattr(user, field, val)


@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=400, detail="Username already taken.")

    user = User(
        email=req.email,
        username=req.username,
        hashed_password=hash_password(req.password),
    )
    _apply_profile_fields(user, req)
    db.add(user)
    db.commit()
    db.refresh(user)

    _sync_conditions(db, user, req.condition_ids, req.custom_conditions)
    db.refresh(user)

    token = create_access_token(user.id, user.email)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    token = create_access_token(user.id, user.email)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.put("/profile", response_model=UserOut)
def update_profile(
    req: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _apply_profile_fields(current_user, req)
    db.commit()
    _sync_conditions(db, current_user, req.condition_ids, req.custom_conditions)
    db.refresh(current_user)
    return UserOut.model_validate(current_user)


@router.get("/conditions")
def list_conditions():
    return PREDEFINED_CONDITIONS
