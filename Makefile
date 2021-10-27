
clean:
	rm resources/*.zip

create-zip: clean
	zip resources/example.zip resources/*

thread-exec: create-zip
	python -m methods.threadPool
	
asyncio-exec: create-zip
	python -m methods.asyncio
