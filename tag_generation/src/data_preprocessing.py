# src/data_preprocessing.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import re

def load_data(filepath):
    return pd.read_csv(filepath)

def clean_text(text):
    """Clean the text by removing non-alphanumeric characters and making it lowercase."""
    text = re.sub(r'\W', ' ', str(text))
    text = text.lower()
    return text

def vectorize_texts(texts):
    """Vectorize the text using TF-IDF Vectorizer."""
    vectorizer = TfidfVectorizer(max_features=2500, min_df=0.01, max_df=0.9, stop_words='english')
    vectorized_texts = vectorizer.fit_transform(texts).toarray()
    return vectorized_texts, vectorizer

def preprocess_data(filepath):
    """Load, clean, and vectorize the text data."""
    data = load_data(filepath)
    data['text'] = data['text'].apply(clean_text)
    texts = data['text']
    labels = data['label']
    
    vectorized_texts, vectorizer = vectorize_texts(texts)
    X_train, X_test, y_train, y_test = train_test_split(vectorized_texts, labels, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test, vectorizer
