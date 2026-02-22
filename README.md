# JobCheque – AI-Based Fake Job Offer Detector

## Project Overview
JobCheque is a machine learning-powered application designed to detect fraudulent or fake job offers. It is engineered with a lightweight Machine Learning approach, making it highly suitable for execution on low-resource hardware. JobCheque identifies deceptive job descriptions combining rule-based heuristics specific to Indian scam patterns and robust ML models like Logistic Regression and Naive Bayes.

## 🚀 Key Features
- **Scam Detection Model**: A lightweight Scikit-learn model analyzing TF-IDF text embeddings.
- **Rules-based Heuristics**: Custom regex-based detection specifically identifying common Indian scam patterns (e.g., upfront payment requests, suspicious email domains).
- **Responsive UI**: A premium, visually distinct frontend built with modern design principles.
- **Microservices Architecture**:
  - `frontend/`: Modern web interface built with React + Vite.
  - `backend/`: Node.js Express server to handle API routing, orchestrate requests, and handle business logic.
  - `ml_service/`: Python/Flask REST API specifically for model inference and training endpoints.
  - `legacy_flask_v1/`: An older, monolithic HTML/Jinja/Flask implementation.

## 💻 System & Hardware Constraints
- **RAM**: Optimized for systems with 4GB strict limits.
- **Storage**: Functional on HDD systems.
- **CPU**: i5 or equivalent.
- **GPU**: Not required (purely CPU-based inference, avoiding resource-heavy Deep Learning models).

## 🛠 Technology Stack
### Frontend
- **Framework**: React.js (via Vite)
- **Styling**: Premium CSS / Modern UI
- **Interactions**: Client-side form validation and dynamic results rendering

### Backend API
- **Runtime**: Node.js & Express.js
- **Responsibilities**: Interface between the web client and the ML service.

### ML Service
- **Engine**: Scikit-learn
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Algorithms**: Logistic Regression / Multinomial Naive Bayes
- **Rule-based Engine**: Regex for detecting scam patterns
- **API Framework**: Python based ML Inference

---

## ⚙️ Setup & Installation

### 1. ML Service (Python Backend)
Provide the prediction capabilities.
```bash
cd ml_service
pip install -r requirements.txt
python train.py      # Generate and save models
python api.py        # Start the ML inference service
```

### 2. Node Backend
Serves as the main gateway for the application.
```bash
cd backend
npm install
npm run dev          # Starts the Express server
```

### 3. Frontend Application
```bash
cd frontend
npm install
npm run dev          # Starts the Vite development server
```

*(Note: If you only want to run the older monolithic version, navigate to `legacy_flask_v1/`, install its `requirements.txt`, run `train_model.py`, and start `app.py`.)*

## 📁 Repository Structure
- `/frontend`: Modern React-based User Interface.
- `/backend`: Node.js middleware orchestrating API requests.
- `/ml_service`: Python environment containing data schemas, Scikit-learn models, training scripts, and an inference API.
- `/legacy_flask_v1`: Original Monolithic Python backend returning rendered HTML templates.
- `/docs`: Additional supporting documents.
