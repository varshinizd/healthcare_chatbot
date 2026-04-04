import json
from pathlib import Path
from fastapi import APIRouter
from backend.models.schemas import FeedbackRequest, FeedbackResponse
from backend.config import settings

router = APIRouter(prefix="/feedback", tags=["feedback"])

FEEDBACK_LOG = Path(settings.LOG_FILE).parent / "feedback_log.jsonl"
FEEDBACK_LOG.parent.mkdir(parents=True, exist_ok=True)


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    entry = {
        "session_id": request.session_id,
        "message_id": request.message_id,
        "score": request.score,
        "comment": request.comment,
    }
    with open(FEEDBACK_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return FeedbackResponse(success=True, message="Feedback recorded. Thank you!")
