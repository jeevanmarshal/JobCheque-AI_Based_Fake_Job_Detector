import pandas as pd
import numpy as np
import re
import joblib
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import classification_report, confusion_matrix

# Initialize NLTK
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

# --- 1. PREPROCESSING ---
def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove punctuation/digits
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

# --- 2. CUSTOM FEATURE EXTRACTOR ---
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
                
            # Feature 3: Free Email (Crude check if not passed separately)
            # In production pipeline, we pass combined strings containing "Email: ..."
            if any(x in text_lower for x in ['@gmail', '@yahoo', '@hotmail', '@rediff']):
                f[2] = 1

            # Feature 4: Salary Promises
            if any(x in text_lower for x in ['daily', 'weekly', 'cash', '5000/day']):
                f[3] = 1
                
            features.append(f)
        return np.array(features)

# --- 3. TRAINING PIPELINE ---

def train_model():
    print("Loading Dataset...")
    df = pd.read_csv('ml_service/data/jobcheq_dataset.csv')
    
    # Create a Rich Text Field for Training (combining structured fields)
    # This ensures model learns from Email and Company Name too
    df['rich_text'] = (
        "Company: " + df['company_name'] + " " +
        "Email: " + df['recruiter_email'] + " " +
        "Job: " + df['job_description']
    )
    
    print("Preprocessing...")
    df['cleaned_text'] = df['rich_text'].apply(clean_text)
    
    X = df['cleaned_text']
    y = df['label'] # 'Fake' or 'Genuine'
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define Pipeline
    # Using FeatureUnion to combine TF-IDF (Text) + RuleBased (Numeric)
    # Note: Naive Bayes handles negative features poorly, but our rules are 0/1 binary, so it's fine.
    
    pipeline = Pipeline([
        ('features', FeatureUnion([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
            ('rules', RuleFeatureExtractor())
        ])),
        ('clf', voting_classifier()) # Ensemble
    ])
    
    print("Training Model...")
    pipeline.fit(X_train, y_train)
    
    print("Evaluating...")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save
    os.makedirs('model_store', exist_ok=True)
    joblib.dump(pipeline, 'model_store/jobcheq_model_v2.pkl')
    print("Model saved to model_store/jobcheq_model_v2.pkl")

def voting_classifier():
    clf1 = LogisticRegression(solver='liblinear', random_state=1)
    clf2 = MultinomialNB()
    return VotingClassifier(estimators=[('lr', clf1), ('nb', clf2)], voting='soft')

if __name__ == "__main__":
    train_model()
