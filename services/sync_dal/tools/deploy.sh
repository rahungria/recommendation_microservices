echo "deploying on production"
.venv/bin/gunicorn -w 1 -b localhost:80 src:app
