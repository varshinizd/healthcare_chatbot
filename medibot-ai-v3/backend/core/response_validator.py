import re
from dataclasses import dataclass, field

DISCLAIMER = (
    "⚠️ Medical Disclaimer: This information is for educational purposes only "
    "and does not constitute medical advice. Please consult a qualified healthcare "
    "professional for diagnosis and treatment."
)

DIAGNOSTIC_PATTERNS = [
    re.compile(r"\byou have\s+(a\s+)?[a-z\s]+(disease|disorder|condition|syndrome|infection)\b", re.IGNORECASE),
    re.compile(r"\byou are diagnosed with\b", re.IGNORECASE),
    re.compile(r"\byou are suffering from\b", re.IGNORECASE),
    re.compile(r"\byour diagnosis is\b", re.IGNORECASE),
    re.compile(r"\bmy diagnosis for you\b", re.IGNORECASE),
]

DOSAGE_PATTERNS = [
    re.compile(r"\btake\s+\d+\s*(mg|ml|mcg|g)\b", re.IGNORECASE),
    re.compile(r"\b\d+\s*(mg|ml|mcg)\s+(twice|once|three times)\s+a\s+day\b", re.IGNORECASE),
]


@dataclass
class ValidationResult:
    is_valid: bool
    issues_found: list[str] = field(default_factory=list)
    corrected_response: str = ""


def validate_response(response: str) -> ValidationResult:
    issues = []
    corrected = response

    # Check for disclaimer
    if "Medical Disclaimer" not in response and "educational purposes only" not in response:
        issues.append("missing_disclaimer")
        corrected = corrected.rstrip() + f"\n\n{DISCLAIMER}"

    # Check for diagnostic language
    for pattern in DIAGNOSTIC_PATTERNS:
        if pattern.search(response):
            issues.append("diagnostic_language_detected")
            break

    # Check for bare dosage numbers without caveat
    for pattern in DOSAGE_PATTERNS:
        if pattern.search(response):
            caveat_present = any(
                kw in response.lower()
                for kw in ["consult", "doctor", "pharmacist", "healthcare", "professional"]
            )
            if not caveat_present:
                issues.append("dosage_without_caveat")
            break

    return ValidationResult(
        is_valid=len(issues) == 0,
        issues_found=issues,
        corrected_response=corrected,
    )
