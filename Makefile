install:
	pip install --no-cache-dir -r requirements.txt

load_data:
	python src/ingest_data.py

preprocess:
	python src/preprocess.py

train:
	python src/train_and_save_model.py

train_and_save_model: load_data preprocess train