import re
from typing import Dict, List, Any

# Risk detection parameters
RISK_THRESHOLD = 0.7
PII_REGEX = r"\b\d{3}-\d{2}-\d{4}\b|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
BIAS_TERMS = ["race", "gender", "religion", "ethnicity", "stereotype", "prejudice", "bias", "discriminate"]
INJECTION_PATTERNS = ["ignore previous", "system prompt", "### instruction", "ignore above", "disregard prior"]

def analyze_prompt(prompt: str) -> Dict[str, Any]:
    """Analyze prompt for risks without storing raw data"""
    risk_factors = []
    
    # PII Detection
    pii_matches = re.findall(PII_REGEX, prompt)
    if pii_matches:
        risk_factors.append({
            "type": "PII", 
            "matches": list(set(pii_matches))[:3],  # Limit matches
            "count": len(pii_matches)
        })
    
    # Bias Detection
    lower_prompt = prompt.lower()
    bias_matches = [term for term in BIAS_TERMS if term in lower_prompt]
    if bias_matches:
        risk_factors.append({
            "type": "BIAS", 
            "matches": list(set(bias_matches))[:5],
            "count": len(bias_matches)
        })
    
    # Injection Detection
    injection_matches = [patt for patt in INJECTION_PATTERNS if patt in lower_prompt]
    if injection_matches:
        risk_factors.append({
            "type": "INJECTION", 
            "matches": injection_matches,
            "count": len(injection_matches)
        })
    
    # Calculate raw risk score (0-1)
    risk_score = min(1.0, 
        len(risk_factors) * 0.3 + 
        sum(factor.get("count", 0) * 0.02 for factor in risk_factors)
    )
    
    return {
        "raw_risk": risk_score,
        "risk_factors": risk_factors,
        "suggestions": generate_suggestions(risk_factors),
        "needs_review": risk_score > RISK_THRESHOLD
    }

def generate_suggestions(risk_factors: List[Dict]) -> List[str]:
    """Generate privacy-preserving suggestions"""
    suggestions = []
    for factor in risk_factors:
        if factor["type"] == "PII":
            suggestions.append("Remove personal identifiers")
        elif factor["type"] == "BIAS":
            suggestions.append("Review for potential bias")
        elif factor["type"] == "INJECTION":
            suggestions.append("Validate prompt intentions")
    return list(set(suggestions))