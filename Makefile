create-env:
	conda env create -f environments/conda.yml

activate-env:
	conda activate rag

install:
	pip install --upgrade pip &&\
		pip install -r environments/requirements.txt

test:
	conda activate rag &&\
		python -m unittest discover tests

format:	
	ruff format *.py 

lint:
	ruff check *.py 

deploy:
	#deploy goes here
		
all: 
	#install lint test format deploy