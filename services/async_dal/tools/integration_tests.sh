echo "running integration tests"
.venv/bin/python -m pytest tests -vv --html-report=./tests/report -m integration
