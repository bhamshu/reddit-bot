from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from joblib import dump
import os
import sys

# Ensure the correct import paths for data_preprocessing
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.data_preprocessing import preprocess_data

def train_and_evaluate_model(data_filepath):
    X_train, X_test, y_train, y_test, _ = preprocess_data(data_filepath)
    
    # Define pipeline including vectorizer and classifier
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('scaler', StandardScaler(with_mean=False)),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    # Define parameter grid for hyperparameter tuning
    param_grid = {
        'tfidf__max_features': [1000, 5000, 10000],
        'classifier__n_estimators': [100, 200, 300],
        'classifier__max_depth': [None, 10, 20]
    }

    # Perform grid search with cross-validation
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    
    # Evaluate the classifier
    predictions = grid_search.predict(X_test)
    print(classification_report(y_test, predictions))
    
    # Save the best model to disk
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models/text_classifier.joblib')
    dump(grid_search.best_estimator_, model_path)
    
    return grid_search.best_estimator_

if __name__ == "__main__":
    data_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/raw_data.csv')
    train_and_evaluate_model(data_filepath)
