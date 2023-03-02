install:
	pip install poetry
	poetry shell
	poetry install

api:
	./prestart.sh
	
clean:
			find . | grep -E "(/__pycache__)" | xargs rm -rf

fix-imports:
			isort .
			
pyre:
		watchman watch .
		pyre
		
server:
			uvicorn app.main:app --reload
