import os
import joblib
from sklearn.model_selection import train_test_split
from utils.project_logger import custom_logger

def load_raw_data():
    """
    Load the raw data from the 'data/raw' directory.
    
    Returns
    -------
    X : numpy array
        The feature matrix of the dataset.
    y : numpy array
        The target values of the dataset.
    """
    custom_logger.info("Loading raw data")
    
    raw_data_directory = 'data/raw'
    X_path = os.path.join(raw_data_directory, 'X.joblib')
    y_path = os.path.join(raw_data_directory, 'y.joblib')
    
    if not os.path.exists(X_path) or not os.path.exists(y_path):
        custom_logger.error("Raw data files not found")
        raise FileNotFoundError("Raw data files not found")
    
    X = joblib.load(X_path)
    y = joblib.load(y_path)
    
    custom_logger.info("Raw data loaded successfully")
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split the data into training and testing sets.
    
    Parameters
    ----------
    X : numpy array
        The feature matrix of the dataset.
    y : numpy array
        The target values of the dataset.
    test_size : float, optional
        The proportion of the dataset to include in the test split (default is 0.2).
    random_state : int, optional
        The seed used by the random number generator (default is 42).
    
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
    custom_logger.info("Splitting data")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    custom_logger.info("Data split successfully")
    return X_train, X_test, y_train, y_test

def save_split_data(X_train, X_test, y_train, y_test):
    """
    Save the split data to the 'data/processed' directory.
    
    Parameters
    ----------
    X_train : numpy array
        The training feature matrix.
    X_test : numpy array
        The testing feature matrix.
    y_train : numpy array
        The training target values.
    y_test : numpy array
        The testing target values.
    """
    custom_logger.info("Saving split data")
    
    # Check if 'data/processed' directory exists and create it if it doesn't
    processed_data_directory = 'data/processed'
    if not os.path.exists(processed_data_directory):
        os.makedirs(processed_data_directory)
        custom_logger.info(f"Created directory: {processed_data_directory}")
    
    # Save the split data to files
    joblib.dump(X_train, os.path.join(processed_data_directory, 'X_train.joblib'))
    joblib.dump(X_test, os.path.join(processed_data_directory, 'X_test.joblib'))
    joblib.dump(y_train, os.path.join(processed_data_directory, 'y_train.joblib'))
    joblib.dump(y_test, os.path.join(processed_data_directory, 'y_test.joblib'))
    custom_logger.info("Split data saved successfully")

if __name__ == "__main__":
    X, y = load_raw_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    save_split_data(X_train, X_test, y_train, y_test)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)