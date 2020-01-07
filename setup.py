#!/usr/bin/env python
from setuptools import setup
# from distutils.command.install import install as _install

setup(
    name='RealSimulator',
    version='0.0.1',
    description='Utility for real data simulator from pure normal and pure tumor data sets',
    author='Takuya Moriyama',
    author_email='moriyama@hgc.jp',
    url='https://github.com/kennethreitz/samplemod',
    license='GPL-3',
    package_dir={'': 'lib'},
    # install_requires = ['PyVCF==0.6.8'],
    packages=['realsimulator',          \
              'realsimulator.command',  \
              'realsimulator.simulator'],
)
