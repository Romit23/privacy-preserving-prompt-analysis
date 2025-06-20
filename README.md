# Privacy-Preserving Prompt Analysis 🔒🤖

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)

A cutting-edge system that securely analyzes LLM input prompts for sensitive information, bias, and prompt injection risks while maintaining mathematical privacy guarantees through differential privacy.


## 📊 System Architecture

```mermaid
graph TB
    A[User Interface<br/>Streamlit Frontend] --> B[FastAPI Backend]
    B --> C[Prompt Analysis Engine]
    C --> D[Sensitive Data Detector]
    C --> E[Bias Analyzer]
    C --> F[Prompt Injection Detector]
    
    D --> G[Differential Privacy Layer]
    E --> G
    F --> G
    
    G --> H[Privacy-Preserving Analytics]
    H --> I[Aggregated Metrics Database]
    
    B --> J[API Endpoints]
    J --> K[External LLM Applications]
    
    L[Docker Container] -.-> A
    L -.-> B
    L -.-> I
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style G fill:#ffebee
    style H fill:#e8f5e8
```

## 🔧 System Components

### **Backend (FastAPI)**
- **Prompt Analysis API**: RESTful endpoints for real-time prompt analysis
- **Privacy Engine**: Differential privacy implementation for secure analytics
- **Risk Assessment**: Multi-layered security and bias detection
- **Data Aggregation**: Privacy-preserving metrics collection
- **Privacy Controls**: Configurable privacy parameters (ε, δ)

### **Frontend (Streamlit)**
- **Interactive Dashboard**: Real-time prompt analysis interface
- **Analytics Visualization**: Aggregated insights with privacy guarantees
- **Privacy Budget(Configurable)**: Calculate no. of prompts which can be used per session after which privacy guarantee decays

### **Core Analysis Modules**
- **Sensitive Data Detection**: PII, credentials, and confidential information
- **Bias Analysis**: Gender, racial, and cultural bias detection
- **Prompt Injection Detection**: Adversarial prompt identification
- **Privacy Metrics**: Differential privacy noise injection

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ (for local development)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Romit23/privacy-preserving-prompt-analysis.git
cd privacy-preserving-prompt-analysis
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional)
nano .env
```

### 3. Docker Deployment (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 4. Access the Application
- **Streamlit Dashboard**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🛠️ Local Development Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Services
```bash
# Terminal 1: Start FastAPI backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Streamlit frontend
streamlit run streamlit_app.py --server.port 8501
```

## 📋 Configuration

### Environment Variables
```bash
# Backend configuration
MONGO_URI=mongodb://admin:password@mongo:27017
PRIVACY_BUDGET=10.0(Configurable)
# You can add epsilon and delta(sensitivity) parameters here as well.For now they are hardcoded in backend.
# Frontend configuration
BACKEND_URL=http://localhost:8000
```

### Privacy Parameters Explained
- **Epsilon (ε)**: Privacy loss parameter. Smaller values = stronger privacy (recommended: 0.1-2.0)
- **Sensitivity**: The maximum change a single individual's data can have on the output. Higher sensitivity requires more noise for the same privacy guarantee.
- **Privacy Budget**: Maximum number of queries before privacy guarantees degrade

## 🔍 API Usage

### Analyze Single Prompt
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is my credit card number 4532-1234-5678-9012?",
    "user_id": "anonymous",
    "privacy_level": "high"
  }'
```

### Response Format
```json
{
  "analysis_id": "uuid-string",
  "risk_score": 0.85,
  "sensitive_data": {
    "detected": true,
    "types": ["credit_card", "pii"],
    "confidence": 0.92
  },
  "bias_analysis": {
    "bias_detected": false,
    "categories": [],
    "confidence": 0.15
  },
  "prompt_injection": {
    "detected": false,
    "attack_type": null,
    "confidence": 0.05
  },
  "privacy_applied": true,
  "epsilon_used": 0.1
}
```


## 🔒 Privacy Guarantees

### Differential Privacy Implementation
1. **Individual Privacy**: No single prompt can be identified from aggregated data
2. **Plausible Deniability**: Results are statistically indistinguishable
3. **Composability**: Multiple queries maintain privacy bounds
4. **Auditable**: Mathematical privacy guarantees with formal proofs

### Technical Details
- **Laplace Mechanism**: For discrete counting queries
- **Privacy Accounting**: Automatic ε-δ budget tracking
- **Noise Calibration**: Adaptive noise based on query sensitivity



## 📚 Documentation

### API Documentation
- **OpenAPI Spec**: Available at `/docs` when running
- **Redoc**: Available at `/redoc` for alternative documentation
- **Postman Collection**: `docs/postman_collection.json`

### Academic Papers
- **Differential Privacy**: [Dwork et al. 2006](https://link.springer.com/chapter/10.1007/11787006_1)
- **Privacy in ML**: [Abadi et al. 2016](https://arxiv.org/abs/1607.00133)
- **Prompt Analysis**: [Wallace et al. 2019](https://arxiv.org/abs/1908.07125)



## 🙏 Acknowledgments

- **Differential Privacy Library**: [Google's DP library](https://github.com/google/differential-privacy)
- **FastAPI Framework**: [Sebastián Ramirez](https://github.com/tiangolo/fastapi)
- **Streamlit**: [Streamlit Team](https://streamlit.io/)
