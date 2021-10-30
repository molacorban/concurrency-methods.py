
SEED_FILE="resources/data-example-100k"
FILES_IN_ZIP=10
URI_PREFIX=s3://concurrency-methods/concurrency-methods/
PLOT_PATH=benchmark/result.png
IMG_APP=ffplay

clean:
	rm resources/*.to_zip
	rm resources/*.zip

clean-s3:
	aws s3 rm $(URI_PREFIX) --recursive

create-plot:
	python3 create_plot.py

create-zip:
	bash create_zip.sh $(FILES_IN_ZIP) $(SEED_FILE)

show-plot: create-plot
	$(IMG_APP) $(PLOT_PATH)

thread-exec:
	python -m methods.threadPool

asyncio-exec:
	python -m methods.asyncio

sequential-exec:
	python -m methods.sequential

