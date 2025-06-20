from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.analysis import analyze_prompt
from app.database import save_analysis, get_dp_analytics
from app.privacy_accountant import accountant
import os

app = FastAPI(
    title="Privacy-Preserving Prompt Analysis API",
    description="API for analyzing LLM prompts with differential privacy",
    version="1.0.0"
)

class PromptRequest(BaseModel):
    prompt: str
    user_id: str = "anonymous"

@app.post("/analyze")
async def analyze_prompt_endpoint(request: PromptRequest):
    try:
        # Allocate privacy budget
        epsilon = accountant.allocate_budget(0.5)
        
        # Perform privacy-preserving analysis
        analysis = analyze_prompt(request.prompt)
        
        # Save results with privacy guarantees
        save_analysis({
            "user_id": request.user_id,
            "prompt_hash": hash(request.prompt),  # Store hash only
            **analysis,
            "epsilon_used": epsilon
        })
        
        return {
            "risk_score": analysis["raw_risk"],
            "risk_factors": analysis["risk_factors"],
            "suggestions": analysis["suggestions"],
            "needs_review": analysis["needs_review"],
            "privacy_guarantee": f"ε={epsilon}"
        }
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/analytics")
async def get_analytics():
    try:
        epsilon = accountant.allocate_budget(0.1)
        analytics = get_dp_analytics(epsilon)
        return {
            **analytics,
            "epsilon_used": epsilon
        }
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.get("/privacy-budget")
async def get_privacy_budget():
    return {
        "total_budget": accountant.global_budget,
        "used_epsilon": accountant.used_epsilon,
        "remaining_budget": accountant.remaining_budget
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)