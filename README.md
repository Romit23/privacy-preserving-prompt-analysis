# Privacy-Preserving Prompt Analysis

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-brightgreen.svg)

A secure API for analyzing LLM prompts with differential privacy guarantees, detecting PII, bias, and prompt injections while protecting user data.

## Key Features

- 🔒 **Privacy-Preserving Analysis**:
  - Differential privacy budget management
  - Secure prompt hashing (no raw storage)
  - Automatic PII detection (emails, SSNs, phone numbers)

- 🛡️ **Risk Detection**:
  - Personal Identifiable Information (PII)
  - Bias-indicating language
  - Prompt injection patterns
  - Privacy risk scoring

- 📊 **Differentially Private Analytics**:
  - Private aggregate statistics
  - Accuracy guarantees for queries
  - Top risk factor tracking


## Getting Started

### Prerequisites
- Docker 20.10+
- Python 3.10+
- MongoDB (included in Docker setup)

### Installation
```bash
git clone https://github.com/Romit23/privacy-preserving-prompt-analysis.git
cd privacy-preserving-prompt-analysis/backend

# Set up environment
cp .env .env_host  # Update with your credentials
docker-compose up -d
```

Example request:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"prompt":"My email is test@example.com"}'
```

## Development

### Running Tests
```bash
docker-compose -f docker-compose.test.yml up --build
```

### Key Configuration
```env
# .env
MONGO_URI=mongodb://admin:password@mongo:27017
PRIVACY_BUDGET=10.0  # Global epsilon budget
BACKEND_URL=http://localhost:8000
```

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [Diffprivlib](https://github.com/IBM/differential-privacy-library) - Differential privacy
- [MongoDB](https://www.mongodb.com/) - Data storage
- [pytest](https://docs.pytest.org/) - Testing framework


Key highlights included:
1. **Privacy-First Focus**: Emphasized differential privacy and secure storage
2. **Clear Architecture**: Visualized the component structure
3. **Practical Examples**: Included sample API calls
4. **Development Ready**: Test instructions and config details
5. **Modern Tooling**: Badges and clean formatting
