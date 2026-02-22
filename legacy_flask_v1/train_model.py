import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Create directories if they don't exist
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Synthetic Dataset for initialization/testing
data = [
    ("We are hiring Data Entry Operators. Salary 50,000. Pay registration fee 500.", "Fake"),
    ("Urgent requirement for Back Office. Work from Home. Call 9999999999.", "Fake"),
    ("Google is hiring Software Engineers. Apply at careers.google.com.", "Real"),
    ("Microsoft requires Data Scientists. Minimum 3 years experience.", "Real"),
    ("Amazon remote job. 5000 per day. No interview. Whatsapp now.", "Fake"),
    ("Join our team as a Junior Developer. Competitive salary and benefits.", "Real"),
    ("Earn 20000 weekly by copy paste work. No skill needed.", "Fake"),
    ("Infosys opening for System Engineer. B.Tech required.", "Real"),
    ("Pay 200 rs for interview card and get job instantly.", "Fake"),
    ("Senior Marketing Manager position at ABC Corp. Send resume to hr@abccorp.com.", "Real")
]

df = pd.DataFrame(data, columns=['text', 'label'])

# Save raw data for reference
df.to_csv('data/synthetic_data.csv', index=False)

print("Training on synthetic data...")

# Split data
X = df['text']
y = df['label']

# Create Pipeline
# using TfidfVectorizer and MultinomialNB as requested (Lightweight)
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
    ('clf', MultinomialNB())
])

# Train
pipeline.fit(X, y)

# Save the pipeline
model_path = 'models/jobcheq_pipeline.pkl'
joblib.dump(pipeline, model_path)

print(f"Model saved to {model_path}")
print("Test predictions:")
print(f"Test: 'Pay money for job' -> {pipeline.predict(['Pay money for job'])[0]}")
print(f"Test: 'Hiring software developer' -> {pipeline.predict(['Hiring software developer'])[0]}")
