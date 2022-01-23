.PHONY: ini install freeze freeze-upgrade login clean

init:
	pip install pip-tools>=6.4.0

install:
	pip install -r requirements.txt

freeze:
	pip-compile

freeze-upgrade:
	pip-compile --upgrade

login:
	python login.py

deploy:
	serverless deploy