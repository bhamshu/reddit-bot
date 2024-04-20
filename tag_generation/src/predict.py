# src/predict.py

from joblib import load
import os
import sys

# Ensure the correct import paths
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.data_preprocessing import clean_text

def load_model_and_vectorizer():
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models/text_classifier.joblib')
    vectorizer_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models/vectorizer.joblib')
    
    classifier = load(model_path)
    vectorizer = load(vectorizer_path)
    
    return classifier, vectorizer

def predict_text(text):
    classifier, vectorizer = load_model_and_vectorizer()
    text = [clean_text(text)]  # Clean the text
    vectorized_text = vectorizer.transform(text).toarray()  # Vectorize the text
    prediction = classifier.predict(vectorized_text)  # Make a prediction
    return prediction[0]

if __name__ == "__main__":
    sample_text = "My boss asks me to present my computer screen all the time."
    prediction = predict_text(sample_text)
    print(f"The predicted category is: {prediction}")
