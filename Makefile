install:
	python -m pip install --upgrade pip
	pip install -r requeiress.txt

lint:
	pylint -d W0122,W0621,R1732,R0903,W0703 *.py */*.py
