import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Initialize NLTK
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    if not isinstance(text, str): return ""
    # 1. Lowercase
    text = text.lower()
    # 2. Remove special chars and digits (keeping basic structure)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # 3. Tokenize & Lemmatize & Stopwords
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

# Ensure model directory exists
os.makedirs('model_store', exist_ok=True)

# Extended Synthetic Dataset (in real scenario, load from CSV)
data = [
    # FAKE
    ("We are hiring Data Entry Operators. Salary 50,000. Pay registration fee 500.", "Fake"),
    ("Urgent requirement for Back Office. Work from Home. Call 9999999999.", "Fake"),
    ("Amazon remote job. 5000 per day. No interview. Whatsapp now.", "Fake"),
    ("Earn 20000 weekly by copy paste work. No skill needed.", "Fake"),
    ("Pay 200 rs for interview card and get job instantly.", "Fake"),
    ("Part time home based job. Investment required 1000rs. Refundable.", "Fake"),
    ("Click this bit.ly link to claim your job offer now! limited time.", "Fake"),
    ("Immediate joining. Security deposit needed for laptop.", "Fake"),
    
    # REAL
    ("Google is hiring Software Engineers. Apply at careers.google.com.", "Genuine"),
    ("Microsoft requires Data Scientists. Minimum 3 years experience.", "Genuine"),
    ("Join our team as a Junior Developer. Competitive salary and benefits.", "Genuine"),
    ("Infosys opening for System Engineer. B.Tech required.", "Genuine"),
    ("Senior Marketing Manager position at ABC Corp. Send resume to hr@abccorp.com.", "Genuine"),
    ("Walk-in interview for Sales Executive at HDFC Bank.", "Genuine"),
    ("Remote Frontend Developer role. React.js and Node.js required.", "Genuine")
]

# Expand dataset slightly for stability
data = data * 5 

df = pd.DataFrame(data, columns=['text', 'label'])

print("Cleaning text...")
df['cleaned_text'] = df['text'].apply(clean_text)

print("Training Advanced ML Model...")

X = df['cleaned_text']
y = df['label']

# Hybrid Model: Logic Regression + Naive Bayes
clf1 = LogisticRegression(random_state=1, solver='liblinear')
clf2 = MultinomialNB()

# Voting Classifier
voting_clf = VotingClassifier(estimators=[('lr', clf1), ('nb', clf2)], voting='soft')

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=3000, ngram_range=(1,2))), # Optimization: Limit features
    ('clf', voting_clf)
])

pipeline.fit(X, y)

# Metrics
# y_pred = pipeline.predict(X)
# print(classification_report(y, y_pred))

model_path = 'model_store/jobcheq_model_v2.pkl'
joblib.dump(pipeline, model_path, compress=3) # Compress to save space
print(f"Model saved to {model_path}")
