
SEED_FILE="resources/data-example"
FILES_IN_ZIP=10
URI_PREFIX=s3://mola-integracoes/concurrency-methods/

clean:
	rm resources/*.to_zip
	rm resources/*.zip

clean-s3:
	aws s3 rm $(URI_PREFIX) --recursive

create-zip:
	bash create_zip.sh $(FILES_IN_ZIP) $(SEED_FILE)

thread-exec:
	python -m methods.threadPool
	
asyncio-exec:
	python -m methods.asyncio

sequential-exec:
	python -m methods.sequential
