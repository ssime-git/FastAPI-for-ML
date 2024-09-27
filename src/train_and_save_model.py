import os
import joblib
import csv
import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from utils.project_logger import custom_logger
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from datetime import datetime

def load_preprocessed_data():
    """
    Load the preprocessed data from the 'data/processed' directory.
    
    Returns
    -------
    X_train : numpy array
        The training feature matrix.
    X_test : numpy array
        The testing feature matrix.
    y_train : numpy array
        The training target values.
    y_test : numpy array
        The testing target values.
    """
    custom_logger.info("Loading preprocessed data")
    
    processed_data_directory = 'data/processed'
    X_train_path = os.path.join(processed_data_directory, 'X_train.joblib')
    X_test_path = os.path.join(processed_data_directory, 'X_test.joblib')
    y_train_path = os.path.join(processed_data_directory, 'y_train.joblib')
    y_test_path = os.path.join(processed_data_directory, 'y_test.joblib')
    
    if not os.path.exists(X_train_path) or not os.path.exists(X_test_path) or \
       not os.path.exists(y_train_path) or not os.path.exists(y_test_path):
        custom_logger.error("Preprocessed data files not found")
        raise FileNotFoundError("Preprocessed data files not found")
    
    X_train = joblib.load(X_train_path)
    X_test = joblib.load(X_test_path)
    y_train = joblib.load(y_train_path)
    y_test = joblib.load(y_test_path)
    
    custom_logger.info("Preprocessed data loaded successfully")
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """
    Train a RandomForest model and record the training time.
    
    Parameters
    ----------
    X_train : numpy array
        The training feature matrix.
    y_train : numpy array
        The training target values.
    
    Returns
    -------
    clf : RandomForestClassifier
        The trained RandomForest classifier.
    """
    import time
    custom_logger.info("Training model")
    
    # Record the start time
    start_time = time.time()
    
    # Train a RandomForest classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Record the end time
    end_time = time.time()
    
    # Calculate the training duration
    training_time = end_time - start_time
    custom_logger.info(f"Model trained successfully in {training_time:.2f} seconds")
    
    return clf, training_time

def save_model(clf, model_path="model/iris_model.pkl"):
    """
    Save the trained model to a file.
    
    Parameters
    ----------
    clf : RandomForestClassifier
        The trained RandomForest classifier.
    model_path : str, optional
        The path where the model will be saved (default is 'model/iris_model.pkl').
    """
    model_directory = os.path.dirname(model_path)
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)
        custom_logger.info(f"Created directory: {model_directory}")
    
    joblib.dump(clf, model_path)
    custom_logger.info(f"Model saved to {model_path}")

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model and return the evaluation metrics.
    
    Parameters
    ----------
    model : sklearn model
        The trained model to evaluate.
    X_test : numpy array
        The testing feature matrix.
    y_test : numpy array
        The testing target values.
    
    Returns
    -------
    metrics : dict
        A dictionary containing the evaluation metrics.
    """
    custom_logger.info("Evaluating model")
    start_time = time.time()
    y_pred = model.predict(X_test)
    end_time = time.time()
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    training_time = end_time - start_time
    
    custom_logger.info(f"Model Accuracy: {accuracy}")
    custom_logger.info("Classification Report:")
    custom_logger.info(report)
    
    metrics = {
        'accuracy': accuracy,
        'classification_report': report,
        'training_time': training_time
    }
    return metrics

def record_metrics(metrics, metrics_path):
    """
    Save the evaluation metrics to a CSV file.
    
    Parameters
    ----------
    metrics : dict
        A dictionary containing the evaluation metrics.
    metrics_path : str
        The path to the metrics CSV file.
    """
    custom_logger.info(f"Saving metrics to {metrics_path}")
    
    # Load existing metrics if the file exists
    if os.path.exists(metrics_path):
        metrics_df = pd.read_csv(metrics_path)
        version = metrics_df['version'].max() + 1
    else:
        metrics_df = pd.DataFrame()
        version = 1
    
    # Add version to metrics
    metrics['version'] = version
    
    # Flatten classification report for CSV
    report = metrics.pop('classification_report')
    for key, value in report.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                metrics[f"{key}_{sub_key}"] = sub_value
        else:
            metrics[key] = value
    
    # Convert metrics to DataFrame and concatenate
    new_metrics_df = pd.DataFrame([metrics])
    metrics_df = pd.concat([metrics_df, new_metrics_df], ignore_index=True)
    
    metrics_df.to_csv(metrics_path, index=False)
    custom_logger.info("Metrics saved successfully")


def train_and_save_model():
    """
    Load the preprocessed data, train a RandomForest model, and save it to a file.
    """
    custom_logger.info("Training and saving model")
    X_train, X_test, y_train, y_test = load_preprocessed_data()
    clf, training_time = train_model(X_train, y_train)
    metrics = evaluate_model(clf, X_test, y_test)
    metrics_path = os.path.join('model', 'metrics.csv')
    record_metrics(metrics, metrics_path)
    save_model(clf)
    print(f"Model training time: {training_time:.2f} seconds. Training data shape: {X_train.shape}, {y_train.shape}")

if __name__ == "__main__":
    train_and_save_model()