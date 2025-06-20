from diffprivlib.mechanisms import Laplace
import numpy as np
import math

# --- Utility Functions ---

def safe_float(value, default=0.0):
    """Convert to float safely, replacing NaN/inf/None with default"""
    try:
        val = float(value)
        if np.isnan(val) or np.isinf(val):
            return default
        return val
    except (TypeError, ValueError):
        return default

def clamp_val(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))

# --- Privatization Functions ---

def privatize_risk_score(value: float, epsilon=0.5) -> float:
    """Privatize risk score in [0.0, 1.0]"""
    safe_val = clamp_val(safe_float(value), 0.0, 1.0)
    mech = Laplace(epsilon=epsilon, sensitivity=1.0)
    return mech.randomise(safe_val)

def privatize_count(value: int, epsilon=0.1) -> float:
    """Privatize count in [0, 1_000_000]"""
    safe_val = clamp_val(safe_float(value), 0.0, 1_000_000.0)
    mech = Laplace(epsilon=epsilon, sensitivity=1.0)
    return mech.randomise(safe_val)

# --- Accuracy Estimation (Optional) ---

def get_accuracy_guarantee(epsilon: float, sensitivity: float, alpha: float = 0.05) -> float:
    """Estimate accuracy (half-width of confidence interval) of Laplace mechanism"""
    if epsilon <= 0 or sensitivity <= 0 or not (0 < alpha < 1):
        return float('nan')
    scale = sensitivity / epsilon
    return scale * math.log(1 / alpha)
