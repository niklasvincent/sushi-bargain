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

postcodes: SHELL:=/bin/bash
postcodes: postcodes.p
	( \
       source ./venv/bin/activate ; \
       ./bin/post-code-lookup-generator.py --database-url https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip --output-directory . ; \
	)

shops: SHELL:=/bin/bash
shops:
	( \
				source ./venv/bin/activate ; \
       ./bin/sushi-store-lookup-generator.py --postcode-database=postcodes.p --output-directory=. ; \
	)

optimise: SHELL:=/bin/bash
optimise:
	( \
				source ./venv/bin/activate ; \
				./bin/sushi-store-optimised-generator.py --input-directory=. --output-directory=. ; \
	)

all: postcodes shops optimise
