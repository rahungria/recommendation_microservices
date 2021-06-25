echo "serving development server"
source .venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=src
export FLASK_RUN_PORT=8002
# FLASK_RUN_HOST=0.0.0.0
python -m flask run --host=0.0.0.0
