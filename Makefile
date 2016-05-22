test:
	./tests/test_postcode.py
	./tests/test_address.py
	./tests/test_itsu.py

postcodes:
	./bin/post-code-lookup-generator.py --database-url https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip --output-directory .

shops:
	./bin/sushi-store-lookup-generator.py --postcode-database=postcodes.p --output-directory=./web

all: postcodes shops
