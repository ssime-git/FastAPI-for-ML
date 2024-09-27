#import logging
#from fastapi import FastAPI
#from prefect_flow import data_pipeline
#
## Configure logging
#logging.basicConfig(
#    filename='app/logs/app.log',  # Log file path
#    level=logging.INFO,               # Log level
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#)
#
## Get the Prefect logger
#prefect_logger = logging.getLogger("prefect")
#
#app = FastAPI()
#
#@app.post("/trigger-pipeline")
#async def trigger_pipeline():
#    logging.info("Triggering the Prefect flow")
#    # Trigger the Prefect flow
#    flow_run = data_pipeline()
#    logging.info("Pipeline triggered successfully")
#    return {"message": "Pipeline triggered"}

from fastapi import FastAPI, HTTPException
from prefect.client import get_client
import logging
import httpx

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            response = await client.get("http://prefect-server:4200/api/deployments/name/data_pipeline/data_pipeline_deployment")
            response.raise_for_status()
            deployment = response.json()

            # Get the flow_id from the deployment
            flow_id = deployment.get('flow_id')
            if not flow_id:
                raise ValueError("Flow ID not found in deployment data")

            # Create a flow run
            response = await client.post(
                "http://prefect-server:4200/api/flow_runs/",
                json={"deployment_id": deployment["id"], "flow_id": flow_id}
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
