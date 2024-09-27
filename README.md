# FastAPI-for-ML
Building a simple FastAPI application for model inference. 

## Usage
```shell
pip install -r requirements.txt
python app.py
```

## Output
![image1.png](./image2.png)
![image2.png](./image1.png)

## Running the prefect container

```sh
docker compose up
```

## trigger the flow

```sh
curl -X POST http://localhost:8000/trigger-pipeline
```