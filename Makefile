build:
	docker build -t topaz:latest -f Dockerfile .

run:
	docker-compose -f docker-compose.yml up

# Cleaning up the python compiled bytecodes
clear-pyc:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf