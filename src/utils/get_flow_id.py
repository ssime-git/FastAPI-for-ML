import requests

# Replace with your Prefect server URL
PREFECT_API_URL = "http://prefect-server:4200/api"

# Replace with your project name
project_name = "data_pipeline"

# Get the project ID
response = requests.get(f"{PREFECT_API_URL}/projects")
projects = response.json()
print(projects)
#project_id = next(project['id'] for project in projects if project['name'] == project_name)
#
## Get the flow ID
#response = requests.get(f"{PREFECT_API_URL}/flows?project_id={project_id}")
#flows = response.json()
#flow_id = next(flow['id'] for flow in flows if flow['name'] == "data_pipeline")
#
#print(f"Flow ID: {flow_id}")