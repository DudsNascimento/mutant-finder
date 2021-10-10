#/bin/bash
export HOSTNAME='localhost'
export FLASK_APP='app'
export JWT_SECRET='D=qw>e(`b1)^zx0'
export JWT_TOKEN_EXPIRES_IN_SECONDS='600'
export MAGNETO_PASSWORD='$2a$12$x8aEcXPpuqOK8.5X7JftbO84CJgk8WSzEJOQJC4i8T/ftXNubVE5K'
export DATABASE_HOST='localhost'
export DATABASE_PORT='5432'
export DATABASE_NAME='mutant_finder'
export DATABASE_USER='postgres'
export DATABASE_PASSWORD='postgres'
cd src
python -m gunicorn -w 1 -b localhost:5000 app:app
cd ..