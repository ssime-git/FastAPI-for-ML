import pandas as pd
import json

def load_and_display_metrics(csv_path, version):
    # Load the CSV file into a DataFrame
    metrics_df = pd.read_csv(csv_path)
    
    # Filter the DataFrame for the specified version
    version_metrics = metrics_df[metrics_df['version'] == version]
    
    if version_metrics.empty:
        print(f"No metrics found for version {version}")
        return
    
    # Convert the DataFrame to a dictionary
    metrics_dict = version_metrics.to_dict(orient='records')[0]
    
    # Convert the dictionary to a JSON string
    metrics_json = json.dumps(metrics_dict, indent=4)
    
    # Print the JSON string
    print(metrics_json)

if __name__ == "__main__":
    # Example usage
    csv_path = 'model/metrics.csv'
    version = 1
    load_and_display_metrics(csv_path, version)