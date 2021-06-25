echo "running unit tests"
.venv/bin/python -m pytest tests -v --html-report=./tests/report -m "not integration"
