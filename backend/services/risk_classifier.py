import re


class RiskClassifier:
    def __init__(self):

        # =====================================================
        # HIGH RISK PATTERNS (regex based)
        # =====================================================
        self.high_risk_patterns = [
            r"\bchest pain\b",
            r"\b(shortness of breath|difficulty breathing|can't breathe)\b",
            r"\bloss of consciousness\b",
            r"\bfainted?\b",
            r"\bstroke\b",
            r"\bface drooping\b",
            r"\barm weakness\b",
            r"\bsevere bleeding\b",
            r"\buncontrolled bleeding\b",
            r"\bheart attack\b",
            r"\banaphylaxis\b",
            r"\bchoking\b",
            r"\bseizure\b",
            r"\bsuicidal?\b",
            r"\bwant to die\b",
            r"\bcough(ing)? blood\b",
            r"\bvomit(ing)? blood\b",
        ]

        # =====================================================
        # MEDIUM RISK KEYWORDS
        # =====================================================
        self.medium_risk_keywords = [
            "persistent",
            "worsening",
            "not getting better",
            "severe pain",
            "high fever"
        ]

    # =====================================================
    # CLASSIFY RISK
    # =====================================================
    def classify_risk(self, text: str) -> str:
        text_lower = text.lower()

        # ---------- HIGH RISK CHECK ----------
        for pattern in self.high_risk_patterns:
            if re.search(pattern, text_lower):
                return "HIGH"

        # ---------- MEDIUM RISK CHECK ----------

        # Fever duration detection
        fever_match = re.search(r"fever.*?(\d+)\s*days?", text_lower)
        if fever_match:
            days = int(fever_match.group(1))
            if days > 3:
                return "MEDIUM"

        # Generic medium risk language
        for keyword in self.medium_risk_keywords:
            if keyword in text_lower:
                return "MEDIUM"

        return "LOW"

    # =====================================================
    # EMERGENCY RESPONSE
    # =====================================================
    def get_emergency_response(self) -> str:
        return """### ⚠️ EMERGENCY ALERT

It sounds like you may be experiencing a medical emergency.

**Please call emergency services (108 in India) or go to the nearest Emergency Room IMMEDIATELY.**

Do not wait for online advice.

Your safety is the top priority."""