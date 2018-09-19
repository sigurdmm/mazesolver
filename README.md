

PYTHONPATH=./ coverage run tests/tests.py
PYTHONPATH=./ python src/main.py

coverage report
coverage report -m

coverage html

