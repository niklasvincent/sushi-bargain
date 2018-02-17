install: SHELL:=/bin/bash
install: requirements.txt
	test -d venv || virtualenv venv
	( \
       source ./venv/bin/activate ; \
       pip install -Ur requirements.txt; \
       python setup.py install; \
    )

test: tox

protobuf:
	protoc -I=. --python_out=sushi-bargain restaurant_data.proto