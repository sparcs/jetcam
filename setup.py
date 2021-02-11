import os
from setuptools import setup, find_packages

install_requires = []
req_file = os.path.sep.join([os.path.realpath(__file__), 'requirements.txt'])
if os.path.isfile(req_file):
	with open(req_file) as f:
		install_requires = f.read().splitlines()

setup(
    name='jetcam',
    version='0.0.0',
    description='An easy to use camera interface for NVIDIA Jetson',
    packages=find_packages(),
    install_requires=install_requires,
)
