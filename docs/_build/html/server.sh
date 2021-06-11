gunicorn -w 1 'sphinxserver:app(home=".")' -b 0.0.0.0:8081

