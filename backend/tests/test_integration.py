import pytest
from unittest.mock import patch
from app.database import save_analysis, get_dp_analytics
from app.analysis import analyze_prompt
from app.dp_utils import privatize_count

class TestDatabaseIntegration:
    """Integration tests for database operations"""
    
    @patch('app.database.db.analyses.insert_one')
    def test_save_analysis(self, mock_insert):
        analysis_data = {
            "user_id": "test_user",
            "prompt_hash": hash("test prompt"),
            "risk_factors": [{"type": "PII"}],
            "raw_risk": 0.8,
            "epsilon_used": 0.5
        }
        result = save_analysis(analysis_data)
        mock_insert.assert_called_once()
    
    @patch('app.database.db.analyses.aggregate')
    @patch('app.database.db.analyses.count_documents')
    @patch('app.database.privatize_count')
    def test_get_dp_analytics(self, mock_privatize, mock_count, mock_aggregate):
        mock_aggregate.return_value = [{"_id": "PII", "count": 10}]
        mock_count.return_value = 100
        mock_privatize.side_effect = lambda x: x + 1  # Simple mock
        
        analytics = get_dp_analytics(epsilon=0.1)
        
        assert "top_risks" in analytics
        assert "total_analyses" in analytics
        assert analytics["total_analyses"] == 101  # 100 + 1 from mock

class TestFullAnalysisIntegration:
    """Integration tests for full analysis pipeline"""
    
    def test_analysis_with_dp(self):
        from app.privacy_accountant import PrivacyAccountant
        accountant = PrivacyAccountant(global_budget=10.0)
        
        prompt = "Email me at test@example.com about gender issues"
        analysis = analyze_prompt(prompt)
        
        assert analysis["raw_risk"] > 0.5
        assert any(f["type"] == "PII" for f in analysis["risk_factors"])
        assert any(f["type"] == "BIAS" for f in analysis["risk_factors"])
        
        # Test that we can allocate budget for this analysis
        epsilon = accountant.allocate_budget(0.5)
        assert epsilon == 0.5