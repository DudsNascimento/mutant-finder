#/bin/bash
export FLASK_APP='app'
cd src
python -m coverage run -m unittest discover
python -m coverage report --omit='*/test*'
cd ..