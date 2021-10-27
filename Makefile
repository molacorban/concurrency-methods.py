
SEED_FILE="resources/data-example"
FILES_IN_ZIP=10

clean:
	rm resources/*.to_zip
	rm resources/*.zip

create-zip:
	bash create_zip.sh $(FILES_IN_ZIP) $(SEED_FILE)

thread-exec: create-zip
	python -m methods.threadPool
	
asyncio-exec: create-zip
	python -m methods.asyncio
