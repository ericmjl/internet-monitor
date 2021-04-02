.PHONY: build clean

clean:
	cd src && rm -rf build && rm -rf dist

build: clean
	cd src && python setup.py bdist_wheel sdist

release: build
	twine upload src/dist/*
