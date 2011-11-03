from setuptools import setup, find_packages
import os

requires = []

try:
    from collections import namedtuple
except ImportError:
    requires.append('namedtuple')

version = '0.1'
description = "GeoHex for Python"
readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
long_description = readme + '\n\n'

setup(name='geohex3',
      version=version,
      description=description,
      long_description=long_description,
      author='Ryo Aita',
      author_email='ryoait@gmail.com',
      url='http://github.com/aita/python-geohex3',
      license='Apache',
      include_package_data=True,
      install_requires=requires,
      classifiers=[
      'License :: OSI Approved :: Apache License',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      packages=['geohex3'],
)

