from sklearn.datasets import load_iris
from utils.project_logger import custom_logger
import joblib
import os

def load_data():
    """
    Load the iris dataset and return it as X and y.
    
    Returns
    -------
    X : numpy array
        The feature matrix of the iris dataset.
    y : numpy array
        The target values of the iris dataset.
    """
    custom_logger.info("Loading data")
    # Load the iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    custom_logger.info("Data loaded successfully")
    return X, y

def save_data(X, y):
    """
    Save the given data to the 'data/raw' directory.
    
    Parameters
    ----------
    X : numpy array
        The feature matrix of the iris dataset.
    y : numpy array
        The target values of the iris dataset.
    """
    custom_logger.info("Saving data")
    
    # Check if 'data/raw' directory exists and create it if it doesn't
    raw_data_directory = 'data/raw'
    if not os.path.exists(raw_data_directory):
        os.makedirs(raw_data_directory)
        custom_logger.info(f"Created directory: {raw_data_directory}")
    
    # Save the data to a file
    joblib.dump(X, os.path.join(raw_data_directory, 'X.joblib'))
    joblib.dump(y, os.path.join(raw_data_directory, 'y.joblib'))
    custom_logger.info("Data saved successfully")

if __name__ == "__main__":
    X, y = load_data()
    save_data(X, y)
    print(X.shape, y.shape)