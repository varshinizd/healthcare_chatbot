import re
import time
from dataclasses import dataclass
from typing import Optional

EMERGENCY_PATTERNS = {
    "cardiac": [
        r"\bchest\s+pain\b",
        r"\bheart\s+attack\b",
        r"\bmyocardial\s+infarction\b",
        r"\bcardiac\s+arrest\b",
        r"\bpalpitation.?\s+and\s+.*(breath|chest)\b",
        r"\bleft\s+arm\s+pain\b",
        r"\bjaw\s+pain\s+and\s+chest\b",
    ],
    "neurological": [
        r"\bstroke\b",
        r"\bface\s+drooping\b",
        r"\barm\s+weakness\b",
        r"\bspeech\s+slurred\b",
        r"\bseizure\b",
        r"\bconvulsion\b",
        r"\bsudden\s+confusion\b",
        r"\bsudden\s+severe\s+headache\b",
        r"\bblurred\s+vision\s+suddenly\b",
        r"\bloss\s+of\s+consciousness\b",
        r"\bpassed\s+out\b",
        r"\bfainted\b",
    ],
    "respiratory": [
        r"\bcan'?t\s+breathe\b",
        r"\bnot\s+breathing\b",
        r"\bstop(ped)?\s+breathing\b",
        r"\bchoking\b",
        r"\bairway\s+blocked\b",
        r"\basthma\s+attack\b",
        r"\bsevere\s+shortness\s+of\s+breath\b",
        r"\bdifficulty\s+breathing\b",
    ],
    "toxicological": [
        r"\boverdose\b",
        r"\bOD\b",
        r"\bingested\s+too\s+much\b",
        r"\bpoisoning\b",
        r"\bpoisoned\b",
        r"\bswallowed\s+.{1,30}(chemical|cleaner|bleach|acid|poison)\b",
        r"\btook\s+too\s+many\s+(pills|tablets|medications)\b",
    ],
    "psychiatric": [
        r"\bsuicid(e|al)\b",
        r"\bwant\s+to\s+(die|kill\s+myself|end\s+my\s+life)\b",
        r"\bkilling\s+myself\b",
        r"\bself.harm\b",
        r"\bcut(ting)?\s+myself\b",
        r"\bno\s+reason\s+to\s+live\b",
        r"\bending\s+it\s+(all)?\b",
        r"\blethal\s+dose\b",
    ],
    "trauma": [
        r"\bsevere\s+bleeding\b",
        r"\bblood\s+everywhere\b",
        r"\bcan'?t\s+stop\s+the\s+bleeding\b",
        r"\bunconscious\b",
        r"\bnot\s+waking\s+up\b",
        r"\bserious\s+accident\b",
        r"\bbroken\s+bone\s+through\b",
        r"\bspinal\s+injury\b",
        r"\bhead\s+trauma\b",
    ],
    "allergic": [
        r"\banaphylaxis\b",
        r"\bsevere\s+allergic\s+reaction\b",
        r"\bthroat\s+swelling\b",
        r"\btongue\s+swelling\b",
        r"\bcan'?t\s+swallow\b",
        r"\bepipen\b",
    ],
}

COMPILED_PATTERNS: dict[str, list] = {
    category: [re.compile(p, re.IGNORECASE) for p in patterns]
    for category, patterns in EMERGENCY_PATTERNS.items()
}


@dataclass
class EmergencyResult:
    is_emergency: bool
    category: Optional[str]
    confidence: float
    matched_pattern: Optional[str]
    latency_ms: float


def detect_emergency(text: str) -> EmergencyResult:
    start = time.perf_counter()
    text_lower = text.lower().strip()

    for category, compiled in COMPILED_PATTERNS.items():
        for pattern in compiled:
            match = pattern.search(text_lower)
            if match:
                latency = (time.perf_counter() - start) * 1000
                return EmergencyResult(
                    is_emergency=True,
                    category=category,
                    confidence=0.95,
                    matched_pattern=pattern.pattern,
                    latency_ms=round(latency, 2),
                )

    latency = (time.perf_counter() - start) * 1000
    return EmergencyResult(
        is_emergency=False,
        category=None,
        confidence=0.0,
        matched_pattern=None,
        latency_ms=round(latency, 2),
    )


EMERGENCY_RESPONSE = (
    "🚨 MEDICAL EMERGENCY DETECTED: Please call 911 (or your local emergency number) "
    "immediately or go to the nearest emergency room. Do not delay seeking emergency care."
)
