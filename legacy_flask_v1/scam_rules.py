import re

class RuleBasedDetector:
    def __init__(self):
        self.scam_keywords = [
            r"registration fee",
            r"security deposit",
            r"money request",
            r"bank details",
            r"whatsapp me",
            r"no interview",
            r"100% genuine",
            r"copy paste",
            r"typing work",
            r"earn .* daily",
            r"pay .* to get .* job"
        ]
    
    def check_rules(self, text):
        text = text.lower()
        flags = []
        confidence_score = 0
        
        for pattern in self.scam_keywords:
            if re.search(pattern, text):
                flags.append(f"Suspicious pattern found: '{pattern}'")
                confidence_score += 20 # Arbitrary score increase for each flag
        
        if confidence_score > 100:
            confidence_score = 100
            
        return {
            "is_suspicious": len(flags) > 0,
            "flags": flags,
            "rule_score": confidence_score
        }
