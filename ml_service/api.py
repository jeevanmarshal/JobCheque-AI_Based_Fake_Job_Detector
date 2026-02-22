from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import whois
import requests
import datetime
from urllib.parse import urlparse
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# Initialize App
app = Flask(__name__)
CORS(app)

# --- Configuration & Setup ---
MODEL_PATH = 'model_store/jobcheq_model_v2.pkl'
model = None

# --- Custom Feature Extractor for Pickle Loading ---
class RuleFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        for text in X:
            f = [0, 0, 0, 0] # [payment, urgency, email_domain, url_risk]
            text_lower = text.lower()
            
            # Feature 1: Payment Keywords
            if any(x in text_lower for x in ['fee', 'money', 'deposit', 'charge', 'investment']):
                f[0] = 1
                
            # Feature 2: Urgency
            if any(x in text_lower for x in ['urgent', 'immediate', 'today', 'now']):
                f[1] = 1
                
            # Feature 3: Free Email
            if any(x in text_lower for x in ['gmail', 'yahoo', 'hotmail', 'rediff']): 
                f[2] = 1

            # Feature 4: Salary Promises
            if any(x in text_lower for x in ['daily', 'weekly', 'cash', '5000day']): 
                f[3] = 1
                
            features.append(f)
        return np.array(features)

# NLTK Setup (Ensure downloaded)
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print(f"Model loaded from {MODEL_PATH}")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None
    else:
        print("Model file not found. Please train the model first.")

# --- Preprocessing ---
def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

# --- Verification Utilities ---
class VerificationUtils:
    def check_whois_age(self, url):
        """Returns risk score (0-100) and details based on domain age"""
        try:
            # Simple caching to avoid spamming WHOIS
            domain = urlparse(url).netloc
            if not domain: domain = url
            
            w = whois.whois(domain)
            creation_date = w.creation_date
            
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if not creation_date:
                return 50, "WHOIS info hidden/unavailable"
                
            age = (datetime.datetime.now() - creation_date).days
            
            if age < 30:
                return 100, f"Critical: Domain is extremely new ({age} days old)"
            elif age < 180:
                return 50, f"Warning: Domain is relatively new ({age} days old)"
            else:
                return 0, f"Domain age is trusted ({age} days old)"
        except Exception as e:
            return 0, f"WHOIS Lookup failed: {str(e)}"

    def check_url_redirects(self, url):
        """Checks for excessive redirects or hidden destinations"""
        if not url.startswith('http'):
            url = 'http://' + url
            
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            chain = [resp.url for resp in response.history] + [response.url]
            
            risk = 0
            details = []
            
            if len(chain) > 3:
                risk = 80
                details.append(f"Suspicious: {len(chain)} redirects detected")
            
            final_domain = urlparse(chain[-1]).netloc
            initial_domain = urlparse(url).netloc
            
            if "bit.ly" in initial_domain or "goo.gl" in initial_domain:
                 details.append(f"Short URL resolves to: {final_domain}")
            
            return risk, "; ".join(details) if details else "Direct URL"
        except:
            return 20, "Could not verify URL reachability"

verifier = VerificationUtils()

# --- Rule-Based Detection Engine (Display Only - Logic moved to model but kept for flags) ---
class RuleEngine:
    def __init__(self):
        self.scam_keywords = [
            r"registration fee", r"security deposit", r"money request",
            r"bank account details", r"pay .* first", r"investment needed",
            r"refundable amount", r"processing fee", r"training fee",
            # India-specific patterns
            r"processing charge", r"pay for id card", r"document verification fee",
            r"gate pass fee", r"laptop charge", r"courier charge"
        ]
        self.urgency_keywords = [
            r"immediate joining", r"start today", r"urgent requirement",
            r"limited slots", r"act fast", r"hiring .* urgent"
        ]
        self.comm_channel_keywords = [
            r"whatsapp interview", r"telegram contact", r"chat only",
            r"no call.*whatsapp", r"message me on telegram"
        ]
        self.suspicious_behaviors = [
            r"offer letter without interview", r"direct joining", 
            r"no interview required", r"100% genuine", r"backdoor entry"
        ]
        self.unrealistic_salary = [
            r"earn .* daily", r"make .* per day", r"weekly payment",
            r"monthly .* 500000", r"part time .* 50000"
        ]
        self.free_email_domains = [
            "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com",
            "rediffmail.com", "yahoo.co.in"
        ]
        self.url_shorteners = [
            "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "is.gd", "t.me", "wa.me"
        ]

    def analyze(self, text, email="", url="", company_name=""):
        flags = []
        text_lower = text.lower()
        
        for pattern in self.scam_keywords:
            if re.search(pattern, text_lower):
                flags.append(f"Suspicious Payment Request: '{pattern.replace(r'', '')}'")

        for pattern in self.comm_channel_keywords:
            if re.search(pattern, text_lower):
                flags.append(f"Unprofessional Contact Method: '{pattern.replace(r'', '')}'")

        for pattern in self.suspicious_behaviors:
            if re.search(pattern, text_lower):
                flags.append(f"Major Red Flag: '{pattern.replace(r'', '')}'")

        for pattern in self.urgency_keywords:
            if re.search(pattern, text_lower):
                flags.append(f"Urgency tactics detected: '{pattern.replace(r'', '')}'")

        for pattern in self.unrealistic_salary:
             if re.search(pattern, text_lower):
                flags.append("Unrealistic Salary Promise")

        if email:
            try:
                domain = email.split('@')[-1].lower()
                if domain in self.free_email_domains:
                    flags.append(f"Unprofessional Email Domain (Free Provider): @{domain}")
                elif company_name:
                    normalized_company = re.sub(r'[^a-zA-Z]', '', company_name.lower())
                    normalized_domain = domain.split('.')[0] 
                    if normalized_company and normalized_company not in domain and domain not in normalized_company:
                         flags.append(f"Potential Domain Mismatch: Email @{domain} vs Company '{company_name}'")
            except:
                pass

        if url:
             for shortener in self.url_shorteners:
                 if shortener in url:
                     flags.append(f"Hidden/Shortened URL detected: {shortener}")

        return flags

rule_engine = RuleEngine()

# --- Routes ---

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        load_model()
        if not model:
            return jsonify({"error": "Model not ready"}), 503

    data = request.json
    raw_text = data.get('text', '')
    
    # Extract Metadata
    email_match = re.search(r'Email: (\S+)', raw_text)
    email = email_match.group(1).strip() if email_match else ""
    
    company_match = re.search(r'Company: (.*?)\n', raw_text)
    company_name = company_match.group(1).strip() if company_match else ""
    if company_name == 'Unknown': company_name = ""
    
    # URL Extraction
    url_match = re.search(r'(https?://[^\s]+)', raw_text)
    url = url_match.group(1) if url_match else ""

    # 1. Prediction (Using Advanced Pipeline: Clean -> TFIDF+Rules -> Model)
    # The pipeline expects an iterable of strings.
    # We must pass the RAW text because the pipeline's first step is text cleaning?
    # NO. In train_advanced.py:
    # df['cleaned_text'] = df['rich_text'].apply(clean_text)
    # pipeline.fit(df['cleaned_text'])
    # So the pipeline EXPECTS CLEANED TEXT.
    
    cleaned = clean_text(raw_text)
    
    try:
        prediction = model.predict([cleaned])[0] 
        proba = model.predict_proba([cleaned])[0]
        confidence = max(proba) * 100
    except Exception as e:
        print(f"ML Error: {e}")
        prediction = "Error"
        confidence = 0

    # 2. Rule-Based Analysis (For Reporting Flags to User)
    indicators = rule_engine.analyze(raw_text, email=email, company_name=company_name, url=url)
    
    # 3. Deep Verification (Network Checks)
    verification_score = 0
    verification_logs = []
    
    if url:
        v_risk, v_log = verifier.check_url_redirects(url)
        if v_risk > 0:
            verification_score += v_risk
            verification_logs.append(v_log)
            indicators.append(v_log)
        
        if "bit.ly" not in url and "goo.gl" not in url:
             w_risk, w_log = verifier.check_whois_age(url)
             if w_risk > 0:
                 verification_score += w_risk
                 verification_logs.append(w_log)
                 indicators.append(w_log)

    # 4. Final Logic
    final_verdict = prediction
    
    critical_keywords = ["registration fee", "security deposit", "investment", "pay for id card", "processing charge"]
    if any(k in raw_text.lower() for k in critical_keywords):
        final_verdict = "Fake"
        confidence = 99.0
    
    if final_verdict == "Genuine":
        if len(indicators) >= 2 or verification_score > 50:
            final_verdict = "Suspicious"
            confidence = 75.0
        if verification_score >= 100:
             final_verdict = "Fake"
             confidence = 90.0

    return jsonify({
        "verdict": final_verdict,
        "confidence": round(confidence, 2),
        "flags": indicators,
        "verification_logs": verification_logs
    })

if __name__ == '__main__':
    load_model()
    app.run(port=5001, debug=True)
