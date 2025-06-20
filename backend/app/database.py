from pymongo import MongoClient
from datetime import datetime
from app.dp_utils import privatize_count,get_accuracy_guarantee
from typing import Dict
import os

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI", "mongodb://admin:password@mongo:27017"))
db = client.prompt_analysis

def save_analysis(data: Dict):
    """Store analysis results with privacy protection"""
    return db.analyses.insert_one({
        "user_id": data["user_id"],
        "prompt_hash": data["prompt_hash"],
        "risk_types": [f["type"] for f in data["risk_factors"]],
        "risk_score": data.get("risk_score", 0.0),
        "epsilon_used": data["epsilon_used"],
        "timestamp": datetime.utcnow()
    })

def get_dp_analytics(epsilon: float):
    """Generate differentially private analytics"""
    # Get true counts
    pipeline = [
        {"$unwind": "$risk_types"},
        {"$group": {"_id": "$risk_types", "count": {"$sum": 1}}}
    ]
    raw_counts = {r["_id"]: r["count"] for r in db.analyses.aggregate(pipeline)}
    
    # Apply differential privacy
    dp_counts = {
        risk_type: privatize_count(count)
        for risk_type, count in raw_counts.items()
    }
    
    # Get privatized total count
    total = privatize_count(db.analyses.count_documents({}))
    
    # Get top risks
    top_risks = sorted(dp_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Calculate accuracy guarantee
    accuracy = get_accuracy_guarantee(epsilon, sensitivity=1.0)
    
    return {
        "top_risks": [{"risk": r[0], "count": r[1]} for r in top_risks],
        "total_analyses": total,
        "accuracy_95": f"±{accuracy:.2f}",
        "privacy_guarantee": f"ε={epsilon}"
    }