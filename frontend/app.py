import streamlit as st
import requests
import os
import time

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
ANALYTICS_REFRESH = 300  # 5 minutes cache

st.set_page_config(
    page_title="Privacy-Preserving Prompt Analyzer",
    page_icon="🔒",
    layout="wide"
)

# Session state for caching
if 'analytics' not in st.session_state:
    st.session_state.analytics = None
    st.session_state.analytics_time = 0

# UI Components
st.title("🔒 Privacy-Preserving Prompt Analyzer")
st.markdown("""
_Analyze LLM prompts for risks without compromising user privacy_  
**Features**:  
- Sensitive information detection
- Bias and fairness analysis
- Prompt injection prevention
- Differential privacy guarantees
""")

# Privacy budget display
def show_privacy_budget():
    try:
        budget = requests.get(f"{BACKEND_URL}/privacy-budget").json()
        remaining = budget['remaining_budget']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Privacy Budget", f"{budget['total_budget']} ε")
        col2.metric("Used Budget", f"{budget['used_epsilon']:.2f} ε")
        
        # Visual progress bar
        progress = min(1.0, budget['used_epsilon'] / budget['total_budget'])
        col3.metric("Remaining Budget", f"{remaining:.2f} ε")
        st.progress(progress, text=f"Privacy budget usage: {progress*100:.1f}%")
        
        if remaining < 1.0:
            st.warning("Privacy budget running low. Contact administrator to reset.")
    except:
        st.error("Could not retrieve privacy budget")

show_privacy_budget()

# Main analysis form
with st.form("analysis_form"):
    prompt = st.text_area("**Enter prompt to analyze:**", height=200,
                         placeholder="Type your LLM prompt here...")
    submitted = st.form_submit_button("🔍 Analyze Prompt")
    
    if submitted and prompt.strip():
        with st.spinner("Analyzing with privacy protection..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={"prompt": prompt}
                ).json()
                
                # Display results
                st.subheader("Analysis Results")
                
                # Risk score visualization
                risk_score = response['risk_score']
                risk_color = "green" if risk_score < 0.4 else "orange" if risk_score < 0.7 else "red"
                st.metric("Risk Score", f"{risk_score:.0%}", 
                         delta_color="off", 
                         help="0-40%: Low risk, 40-70%: Medium risk, 70-100%: High risk")
                st.progress(risk_score, text=f"Risk level: {risk_score:.0%}")
                
                # Risk details
                if response.get("risk_factors"):
                    st.warning("**⚠️ Risks Detected**")
                    for factor in response["risk_factors"]:
                        with st.expander(f"{factor['type']} risk (found {len(factor['matches'])} instances)"):
                            st.caption(f"Matched terms: {', '.join(factor['matches'])[:200]}")
                else:
                    st.success("✅ No significant risks detected")
                
                # Suggestions
                if response.get("suggestions"):
                    st.info("**💡 Recommendations**")
                    for suggestion in response["suggestions"]:
                        st.write(f"- {suggestion}")
                
                # Privacy guarantee
                if response.get("privacy_guarantee"):
                    st.caption(f"🔐 Privacy guarantee: {response['privacy_guarantee']} (your prompt was not stored)")
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

# Analytics section
st.divider()
st.subheader("Aggregate Insights")

# Refresh analytics if stale
current_time = time.time()
if current_time - st.session_state.analytics_time > ANALYTICS_REFRESH:
    try:
        analytics = requests.get(f"{BACKEND_URL}/analytics").json()
        st.session_state.analytics = analytics
        st.session_state.analytics_time = current_time
    except:
        st.error("Could not load analytics")

if st.button("🔄 Refresh Analytics", help="Get latest insights with privacy protection"):
    try:
        analytics = requests.get(f"{BACKEND_URL}/analytics").json()
        st.session_state.analytics = analytics
        st.session_state.analytics_time = time.time()
        st.success("Analytics refreshed with privacy protection")
    except:
        st.error("Could not refresh analytics")

if st.session_state.analytics:
    analytics = st.session_state.analytics
    st.caption(f"**Privacy Guarantee**: {analytics.get('privacy_guarantee', 'ε=0.1')} | "
               f"**Accuracy**: {analytics.get('accuracy_95', '±N/A')} (95% confidence)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Prompts Analyzed", int(analytics["total_analyses"]))
    
    with col2:
        st.metric(
    "Most Common Risk",
    analytics["top_risks"][0]["risk"] if analytics["top_risks"] else "None",
    delta=f"{int(analytics['top_risks'][0]['count'])} instances" if analytics["top_risks"] else ""
)
    
    # Risk distribution chart
    if analytics["top_risks"]:
        st.bar_chart(
            {r["risk"]: r["count"] for r in analytics["top_risks"]},
            use_container_width=True,
            color="#FF4B4B"
        )
    
    # Data table
    with st.expander("View detailed risk distribution"):
        st.table(analytics["top_risks"])
else:
    st.info("Analytics data not available. Click 'Refresh Analytics' to generate insights.")