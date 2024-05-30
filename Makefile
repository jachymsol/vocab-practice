install:
	python -m pip install virtualenv
	python -m virualenv venv
	source venv/bin/activate && python -m pip install -e .

test: 
	python -m pytest

run:
	docker run -v $(pwd):/apps/Vocabulary_Practice -p 3030:3030 anvilworks/anvil-app-server --app Vocabulary_Practice
