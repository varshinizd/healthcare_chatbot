import time
from dataclasses import dataclass
from functools import lru_cache
from backend.config import settings
from backend.core.gemini_client import gemini_client
import asyncio


@dataclass
class ClassificationResult:
    is_medical: bool
    confidence: float
    category: str
    latency_ms: float


_cache: dict = {}


async def classify_query(query: str) -> ClassificationResult:
    start = time.perf_counter()
    cache_key = query.lower().strip()

    if cache_key in _cache:
        cached = _cache[cache_key]
        latency = (time.perf_counter() - start) * 1000
        return ClassificationResult(
            is_medical=cached["is_medical"],
            confidence=cached["confidence"],
            category=cached["category"],
            latency_ms=round(latency, 2),
        )

    if len(_cache) > 256:
        oldest_key = next(iter(_cache))
        del _cache[oldest_key]

    result = await gemini_client.classify_query(query)

    _cache[cache_key] = result

    confidence = result["confidence"]
    is_medical = result["is_medical"]

    # Fail-open: if confidence is below threshold, allow the query
    if confidence < settings.MIN_CONFIDENCE_SCORE:
        is_medical = True

    latency = (time.perf_counter() - start) * 1000
    return ClassificationResult(
        is_medical=is_medical,
        confidence=confidence,
        category=result["category"],
        latency_ms=round(latency, 2),
    )
