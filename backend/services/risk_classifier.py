import re

class RiskClassifier:
    def __init__(self):
        self.high_risk_keywords = [
            "chest pain", "difficulty breathing", "shortness of breath", 
            "loss of consciousness", "fainted", "stroke", "face drooping", 
            "arm weakness", "severe bleeding", "uncontrolled bleeding",
            "heart attack", "anaphylaxis", "choking", "seizure", "suicide","coughing blood",
        ]
        
        self.medium_risk_keywords = [
            "persistent", "worsening", "not getting better"
        ]

    def classify_risk(self, text: str) -> str:
        text_lower = text.lower()
        
        # 1. Check High Risk
        for keyword in self.high_risk_keywords:
            if keyword in text_lower:
                return "HIGH"
        
        # 2. Check Medium Risk
        # Fever > 3 days
        # Matches: "fever for 4 days", "fever since 5 days ago", "fever > 3 days"
        fever_match = re.search(r"fever.*(\d+)\s*days?", text_lower)
        if fever_match:
            days = int(fever_match.group(1))
            if days > 3:
                return "MEDIUM"
                
        for keyword in self.medium_risk_keywords:
            if keyword in text_lower:
                return "MEDIUM"
                
        # 3. Default Low
        return "LOW"

    def get_emergency_response(self) -> str:
        return """### ⚠️ EMERGENCY ALERT
        
It sounds like you may be experiencing a medical emergency. 

**Please call emergency services (108 or your local equivalent) or go to the nearest Emergency Room IMMEDIATELY.**

I cannot provide further assistance for this situation. Your safety is the top priority."""
