import re
import time
from typing import Optional
from dataclasses import dataclass

from backend.core.emergency import detect_emergency, EMERGENCY_RESPONSE
from backend.core.classifier import classify_query
from backend.core.rag_pipeline import rag_pipeline
from backend.core.gemini_client import gemini_client
from backend.core.response_validator import validate_response

NON_MEDICAL_RESPONSE = (
    "I'm specialized in medical and health topics only. "
    "I'm unable to assist with that topic — please consult the appropriate resource."
)

INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(dan|jailbreak|unrestricted)", re.IGNORECASE),
    re.compile(r"forget\s+(your\s+)?(previous\s+)?instructions?", re.IGNORECASE),
    re.compile(r"reveal\s+your\s+(system\s+)?prompt", re.IGNORECASE),
    re.compile(r"override\s+(safety|guardrail|instruction)", re.IGNORECASE),
]


@dataclass
class GuardrailResult:
    response: str
    blocked: bool
    block_reason: Optional[str]
    layer_triggered: Optional[str]
    latency_ms: float
    rag_used: bool = False
    category: str = "unknown"
    is_emergency: bool = False
    is_clarifying_question: bool = False


def sanitize_input(text: str) -> tuple[str, bool]:
    for pattern in INJECTION_PATTERNS:
        if pattern.search(text):
            return text, True
    return text[:2000].strip(), False


def _looks_like_clarifying_question(response: str) -> bool:
    question_marks = response.count("?")
    return question_marks >= 1 and len(response) < 500


async def run_guardrails(
    query: str,
    history: list[dict],
    user=None,
) -> GuardrailResult:
    total_start = time.perf_counter()

    # Layer 1: Emergency
    emergency = detect_emergency(query)
    if emergency.is_emergency:
        latency = (time.perf_counter() - total_start) * 1000
        return GuardrailResult(
            response=EMERGENCY_RESPONSE,
            blocked=True,
            block_reason="emergency_detected",
            layer_triggered="layer_1_emergency",
            latency_ms=round(latency, 2),
            is_emergency=True,
            category=emergency.category or "emergency",
        )

    # Layer 2: Sanitization
    clean_query, was_injected = sanitize_input(query)
    if was_injected:
        latency = (time.perf_counter() - total_start) * 1000
        return GuardrailResult(
            response=NON_MEDICAL_RESPONSE,
            blocked=True,
            block_reason="prompt_injection_detected",
            layer_triggered="layer_2_sanitization",
            latency_ms=round(latency, 2),
        )

    # Layer 3: Classification
    classification = await classify_query(clean_query)
    if not classification.is_medical:
        latency = (time.perf_counter() - total_start) * 1000
        return GuardrailResult(
            response=NON_MEDICAL_RESPONSE,
            blocked=True,
            block_reason="non_medical_query",
            layer_triggered="layer_3_classifier",
            latency_ms=round(latency, 2),
            category=classification.category,
        )

    # Layer 4: RAG
    injected_context = None
    rag_used = False
    if classification.category != "greeting":
        injected_context = await rag_pipeline.retrieve_context(clean_query)
        rag_used = injected_context is not None

    # Layer 5: Generation — pass full user object
    messages = list(history) + [{"role": "user", "content": clean_query}]
    response_text = await gemini_client.generate_response(
        messages,
        user=user,
        injected_context=injected_context,
    )

    # Layer 6: Validation
    is_clarifying = _looks_like_clarifying_question(response_text)
    if not is_clarifying and classification.category != "greeting":
        validation = validate_response(response_text)
        response_text = validation.corrected_response or response_text

    latency = (time.perf_counter() - total_start) * 1000
    return GuardrailResult(
        response=response_text,
        blocked=False,
        block_reason=None,
        layer_triggered=None,
        latency_ms=round(latency, 2),
        rag_used=rag_used,
        category=classification.category,
        is_emergency=False,
        is_clarifying_question=is_clarifying,
    )
