setup:
	./setup.sh

start:
	uvicorn main:app --reload

test:
	pytest