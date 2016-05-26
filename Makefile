install: SHELL:=/bin/bash
install: requirements.txt
	test -d venv || virtualenv venv
	( \
       source ./venv/bin/activate ; \
       pip install -Ur requirements.txt; \
    )

test: SHELL:=/bin/bash
test:
	( \
       source ./venv/bin/activate ; \
	    ./tests/test_postcode.py ; \
	    ./tests/test_address.py ; \
	    ./tests/test_itsu.py \
	)

postcodes: postcodes.p
	./bin/post-code-lookup-generator.py --database-url https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip --output-directory .

shops:
	./bin/sushi-store-lookup-generator.py --postcode-database=postcodes.p --output-directory=./web

optimise:
	./bin/sushi-store-optimised-generator.py --input-directory=./web --output-directory=./web

all: postcodes shops optimise
