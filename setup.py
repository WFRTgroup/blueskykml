#!/usr/bin/env python

from setuptools import setup, find_packages

from blueskykml import __version__

test_requirements = []
with open('requirements-test.txt') as f:
    test_requirements = [r for r in f.read().splitlines()]

setup(
    name='blueskykml',
    version=__version__,
    author='Anthony Cavallaro, Ken Craig, John Stilley, Joel Dubowy',
    author_email='jdubowy@gmail.com', # STI's email addresses
    packages=find_packages(),
    package_data={
        'blueskykml': [
            'assets/*.png',
            'config/*.ini'
        ]
    },
    scripts=[
        'bin/makedispersionkml'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Operating System :: POSIX",
        "Operating System :: MacOS"
    ],
    url='https://github.com/pnwairfire/blueskykml/',
    description='Package for creating kmls from BlueSky smoke dispersion output.',
    install_requires=[
        "GDAL==1.11.2",
        "numpy==1.9.2",
        "Pillow==2.8.1",
        "matplotlib==1.4.3"
    ],
    tests_require=test_requirements
)
