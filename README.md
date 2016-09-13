# live_stream

# Setup virtual environment
pip install virtualenv
virtualenv develop
source develop/bin/activate
./develop/bin/python setup.py develop
deactivate

# Build
python setup.py sdist

# Install as non root user
pip install --user dist/livestream-0.x.tar.gz

# Run from the command line
main.py
