
api:
	./prestart.sh
	
clean:
			find . | grep -E "(/__pycache__)" | xargs rm -rf

server:
			uvicorn app.main:app --reload