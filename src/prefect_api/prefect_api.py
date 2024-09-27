from fastapi import FastAPI, HTTPException
from prefect.client import get_client
import logging
import httpx
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# New addition: Get Prefect API URL from environment variable
PREFECT_API_URL = os.getenv('PREFECT_API_URL', 'http://prefect-server:4200/api')
PREFECT_API_KEY = os.getenv('PREFECT_API_KEY', '')  # Leave empty if not using authentication

@app.get("/")
async def root():
    return {"message": "Prefect API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/run-flow/")
async def run_flow():
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # Get the deployment by name
            response = await client.get(f"{PREFECT_API_URL}/deployments/name/data_pipeline/data_pipeline_deployment")
            response.raise_for_status()
            deployment = response.json()

            # Get the deployment_id from the deployment
            deployment_id = deployment.get('id')
            if not deployment_id:
                raise ValueError("Deployment ID not found in deployment data")

            # Prepare headers
            headers = {}
            if PREFECT_API_KEY:
                headers["Authorization"] = f"Bearer {PREFECT_API_KEY}"

            # Prepare payload
            payload = {
                "name": "data-pipeline-flow-run",
                # Add any parameters your flow needs here
            }

            # Create a flow run using the new method
            response = await client.post(
                f"{PREFECT_API_URL}/deployments/{deployment_id}/create_flow_run",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            flow_run = response.json()

            logger.info(f"Flow run created: {flow_run['id']}")
            return {"message": "Flow run created", "flow_run": flow_run}
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e.response.status_code} {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Error triggering flow: {e.response.text}")
    except ValueError as e:
        logger.error(f"Value error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error triggering flow: {str(e)}")

# You can keep your existing flow run status endpoint as is