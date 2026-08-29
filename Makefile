.PHONY: install build run test clean docker-build docker-run

install:
	pip install -r requirements.txt

build:
	python data/init_db.py

run:
	python run.py

test:
	python -m unittest discover -s backend/tests

docker-build:
	docker build -t lifeos .

docker-run:
	docker run -p 5000:5000 lifeos

clean:
	rm -rf __pycache__ backend/__pycache__ backend/*/__pycache__ .pytest_cache
