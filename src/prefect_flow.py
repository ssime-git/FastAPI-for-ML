from prefect import task, flow
from ingest_data import load_data, save_data
from preprocess import load_raw_data, split_data, save_split_data
from prefect.logging import get_run_logger

@task
def ingest_data_task():
    X, y = load_data()
    save_data(X, y)
    return X.shape, y.shape

@task
def preprocess_data_task():
    X, y = load_raw_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    save_split_data(X_train, X_test, y_train, y_test)
    return X_train.shape, X_test.shape, y_train.shape, y_test.shape

@flow(name="data_pipeline")
def data_pipeline():
    ingest_data_result = ingest_data_task()
    preprocess_data_result = preprocess_data_task()
    print("Ingest data result:", ingest_data_result)
    print("Preprocess data result:", preprocess_data_result)

if __name__ == "__main__":
    data_pipeline()