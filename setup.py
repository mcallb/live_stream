from setuptools import setup

setup(name='livestream',
    version='0.12',
    description='Monitors a Youtube live stream',
    url='https://github.com/mcallb/live_stream',
    author='Brian McAllister',
    author_email='mcallb@gmail.com',
    license='MIT',
    packages=['live_stream'],
    zip_safe=False,
    install_requires = ['retrying','google-api-python-client','oauth2client','httplib2','requests','argparse'],
    scripts = ["live_stream/monitor.py",])