from flask import Flask, render_template, request, jsonify
import joblib
import os
from scam_rules import RuleBasedDetector

app = Flask(__name__)

# Load Model
MODEL_PATH = 'models/jobcheq_pipeline.pkl'
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        model = None
        print("Model not found. Please run train_model.py first.")
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

rule_detector = RuleBasedDetector()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    results = {
        "prediction": "Unknown",
        "confidence": 0,
        "flags": [],
        "overall_status": "Unknown"
    }

    # 1. Rule-based check
    rule_res = rule_detector.check_rules(text)
    results['flags'] = rule_res['flags']
    
    # 2. ML Prediction
    ml_confidence = 0
    if model:
        prediction = model.predict([text])[0]
        # Get probability if model supports it
        try:
            proba = model.predict_proba([text])[0]
            ml_confidence = max(proba) * 100
        except:
            ml_confidence = 0 # Naive Bayes usually supports predict_proba
        
        results['prediction'] = prediction
        results['ml_confidence'] = round(ml_confidence, 2)
    else:
        results['prediction'] = "Model Unavailable"

    # 3. Combine Logic
    # If rules find it suspicious, we lean towards Fake
    if rule_res['is_suspicious']:
        results['overall_status'] = "Fake"
        results['confidence'] = max(rule_res['rule_score'], results.get('ml_confidence', 0))
    else:
        results['overall_status'] = results['prediction']
        results['confidence'] = results.get('ml_confidence', 0)

    # If ML says Real but low confidence? 
    # For now, let's just return what we have.
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
