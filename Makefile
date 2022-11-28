install:
	python setup.py install

clean:
	rm -rf __pycache__ dist kgcreator.egg-info build
	rm -rf kgcreator/__pycache__ tests/__pycache__
