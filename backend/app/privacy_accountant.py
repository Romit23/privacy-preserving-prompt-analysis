import os

class PrivacyAccountant:
    def __init__(self, global_budget: float = 10.0):
        self.global_budget = global_budget
        self.used_epsilon = 0.0
    
    @property
    def remaining_budget(self) -> float:
        return self.global_budget - self.used_epsilon
    
    def allocate_budget(self, requested_epsilon: float) -> float:
        """Allocate privacy budget with checks"""
        if requested_epsilon <= 0:
            raise ValueError("Epsilon must be positive")
        
        if self.remaining_budget < requested_epsilon:
            raise ValueError(
                f"Privacy budget exceeded. Requested: {requested_epsilon}, "
                f"Available: {self.remaining_budget:.2f}"
            )
        
        self.used_epsilon += requested_epsilon
        return requested_epsilon

# Initialize global privacy accountant
accountant = PrivacyAccountant(global_budget=float(os.getenv("PRIVACY_BUDGET", "10.0")))